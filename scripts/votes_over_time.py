import pandas as pd

from load_data import load_votes, load_postings


def create_votes_df() -> pd.DataFrame:
    votes = load_votes()
    postings = load_postings()
    merged = pd.merge(votes, postings, on="ID_Posting")
    merged["Vote"] = merged["VotePositive"] - merged["VoteNegative"]
    renamed = merged.rename(columns={"UserCommunityName_x": "UserPost", "UserCommunityName_y": "UserVote"})
    return renamed[["UserPost", "UserVote", "VoteCreatedAt", "Vote"]]


def save_votes_df(df: pd.DataFrame, path="../output/") -> None:
    df.to_csv(path + "user_votes.csv", index=False)


def load_votes_df(path="../output/") -> None:
    pd.read_csv(path + "user_votes.csv")


if __name__ == '__main__':
    df = load_votes_df()
    save_votes_df(df)