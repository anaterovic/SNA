import pandas as pd
import numpy as np


def load_votes(path="../input/"):
    votes_1 = pd.read_csv(path + 'Votes_01052019_15052019.csv', sep=';')
    votes_2 = pd.read_csv(path + 'Votes_16052019_31052019.csv', sep=';')
    votes = pd.concat([votes_1, votes_2]).astype({"VoteCreatedAt": "datetime64"})
    print("Votes loaded")
    return votes


def load_postings(path="../input/"):
    postings_1 = pd.read_csv(path + '/Postings_01052019_15052019.csv', sep=';')
    postings_2 = pd.read_csv(path + '/Postings_16052019_31052019.csv', sep=';')
    postings = pd.concat([postings_1, postings_2]).astype({"PostingCreatedAt": "datetime64"})
    print("Postings loaded")
    return postings


def get_middle_day(date_series):
    date_series = date_series.dt.date
    time_span = date_series.max() - date_series.min()
    half_time_span = time_span/2
    middle = (date_series.min() + half_time_span)
    return middle

def _apply_bidirectionality(df, on="VoteCreatedAt"):
    """Here we account for bidirectionality of the contact pairs. The problem is that if user A comments user B's post,
     but user B previously commented user A's post we have 2 rows with (eventually) different dates. We take the minimum and leciographycally sort the usernames for enabling joining"""
    inv_df = (df.merge(df, left_on=["UserCommunityName_x", "UserCommunityName_y"], right_on=["UserCommunityName_y", "UserCommunityName_x"], suffixes=("", "_inv"), how="left"))
    inv_df[[f"{on}_inv",f"{on}"]] = inv_df[[f"{on}_inv",f"{on}"]].fillna(pd.to_datetime("2050-01-01", format="%Y-%m-%d").date())
    inv_df[f"{on}_bidirectional"] = inv_df[[f"{on}_inv",on]].min(axis=1)
    inv_df[["UserCommunityName_x", "UserCommunityName_y"]] = np.sort(inv_df[["UserCommunityName_x", "UserCommunityName_y"]], axis=1)
    return inv_df[["UserCommunityName_x", "UserCommunityName_y", f"{on}_bidirectional"]].drop_duplicates()

def _subset_min_interaction(votes, postings, num_days_min, interaction_type):
    v = votes[["UserCommunityName","VoteCreatedAt"]].rename(columns={"VoteCreatedAt":"CreatedAt"})
    p = postings[["UserCommunityName", "PostingCreatedAt"]].rename(columns={"PostingCreatedAt":"CreatedAt"})
    df = [v,p]
    if interaction_type == "votes":
        df=[v]
    if interaction_type == "postings":
        df=[p]
        
    full_df = pd.concat(df)
    num_days_interacted = full_df.groupby(["UserCommunityName",full_df.CreatedAt.dt.day]).size().reset_index()\
                    .groupby("UserCommunityName").size().reset_index()

    user_subset_days_interacted = num_days_interacted[num_days_interacted[0] >= num_days_min].UserCommunityName.unique()
    return user_subset_days_interacted

def get_first_contact_df(votes, postings, interaction_type):
    # Find u-u tuples with their first date of interaction by vote
    first_contact_vote_pairs = (votes[["UserCommunityName", "UserCreatedAt", "ID_Posting", "VoteCreatedAt"]]
    .merge(postings[["ID_Posting", "UserCommunityName", "UserCreatedAt"]], on=["ID_Posting"], how="left")
    [["UserCommunityName_x", "UserCommunityName_y", "VoteCreatedAt"]]
    .sort_values("VoteCreatedAt")
    .groupby(["UserCommunityName_x", "UserCommunityName_y"])
    .first()
    .reset_index())
    
    first_contact_vote_pairs_bd = _apply_bidirectionality(first_contact_vote_pairs, "VoteCreatedAt")
    if interaction_type == "votes":
        first_contact_vote_pairs_bd["first_contact"] = first_contact_vote_pairs_bd["VoteCreatedAt_bidirectional"]
        return first_contact_vote_pairs_bd
    
    # find u-u tuples with their first date of interaction by reply
    first_contact_reply_pairs = (postings.dropna(subset=["ID_Posting_Parent"])[
    ["UserCommunityName", "ID_Posting_Parent", "PostingCreatedAt"]]
    .merge(postings[["ID_Posting", "UserCommunityName"]], left_on=["ID_Posting_Parent"], right_on=["ID_Posting"], how="left")
    [["UserCommunityName_x", "UserCommunityName_y", "PostingCreatedAt"]]
    .sort_values("PostingCreatedAt")
    .groupby(["UserCommunityName_x", "UserCommunityName_y"])
    .first()
    .reset_index())
    
    first_contact_reply_pairs_bd = _apply_bidirectionality(first_contact_reply_pairs, "PostingCreatedAt")
    if interaction_type == "replies":
        first_contact_reply_pairs_bd["first_contact"] = first_contact_reply_pairs_bd["PostingCreatedAt_bidirectional"]
        return first_contact_reply_pairs_bd
    
    
    # If we want to consider both, we take the minimum of the two
    fist_contact = (first_contact_reply_pairs_bd.merge(first_contact_vote_pairs_bd, on=["UserCommunityName_x", "UserCommunityName_y"], how="outer")
    .fillna(pd.to_datetime("2050-01-01", format="%Y-%m-%d").date())) # We set a date in the future to avoid problems with the min function
    fist_contact["first_contact"] = fist_contact[[
    "PostingCreatedAt_bidirectional", "VoteCreatedAt_bidirectional"]].min(axis=1)
    return fist_contact



    
def subset_users(votes, postings, interaction_type, num_days_min=None, firt_interaction_middle=False ):
    """Subset users based on the number of days they interacted with the community and only keep users that are involved in a
    first contact with someone in the middle day of the interval

    Args:
        votes (_type_): votes df
        postings (_type_): postings df
        num_days_min (_type_, optional): Number of days a user has to have posted in the interval. Defaults to None.
        interaction_type (_type_, optional): If set, filter users that interacted in the middle of the interval. We can define the type of interaction (votes, replies, both). Defaults to None.

    Returns:
        _type_: a dataframe of users with shape (n_users, )
    """
    subset_days_interacted, selected_users_middle = None, None
    if num_days_min:
        subset_days_interacted = _subset_min_interaction(votes, postings, num_days_min, interaction_type)
    if firt_interaction_middle:
        first_contact = get_first_contact_df(votes, postings, interaction_type)
        middle = get_middle_day(first_contact["first_contact"])
        first_contact_filtered = first_contact[first_contact["first_contact"].dt.date == middle][["UserCommunityName_x", "UserCommunityName_y", "first_contact"]]
        selected_users_middle = pd.concat([first_contact_filtered["UserCommunityName_x"], first_contact_filtered["UserCommunityName_y"]]).drop_duplicates() # middle interval subset

        first_contact_filtered[["UserCommunityName_x", "UserCommunityName_y"]].to_csv(
            f'uu_tuples/uu_first_contact_tuples_{interaction_type}.csv', index=False)

        first_contact_export = (first_contact_filtered[["UserCommunityName_x", "UserCommunityName_y"]]
                            .assign(UserCommunityName_x=lambda x: "user_" + x.UserCommunityName_x)
                            .assign(UserCommunityName_y=lambda x: "user_" + x.UserCommunityName_y))
                        
    if num_days_min and firt_interaction_middle:
        return selected_users_middle[selected_users_middle.isin(subset_days_interacted)], first_contact_export
    
    return selected_users_middle or subset_days_interacted, first_contact_export
