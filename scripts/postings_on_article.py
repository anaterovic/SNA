###
# Dont work on my hardware
###

import pandas as pd

from load_data import load_postings


def create_df_postings_on_article() -> pd.DataFrame:
    postings = load_postings()

    postings_reduced = postings[["ID_Posting", "ID_Article", "UserCommunityName", "PostingCreatedAt"]]
    articles = postings_reduced["ID_Article"].drop_duplicates().values

    dfs = []
    print("Start merging: ")
    for i, article in enumerate(articles):
        postings_article = postings_reduced[postings_reduced["ID_Article"] == article]
        merged = pd.merge(postings_article, postings_article, on="ID_Article")
        dfs.append(merged[["UserCommunityName_x", "UserCommunityName_y", "PostingCreatedAt_x", "PostingCreatedAt_y",
                           "ID_Article"]].rename(columns={
            "UserCommunityName_x": "User1",
            "UserCommunityName_y": "User2",
            "PostingCreatedAt_x": "PostingUser1CreatedAt",
            "PostingCreatedAt_y": "PostingUser2CreatedAt",
        }))

        print("Merging: " + str((float(i) / float(len(articles))) * 100.0) + "%", end="\r")

    return pd.concat(dfs)


def save_df_direct_comments(path="../output/") -> None:
    df = create_df_postings_on_article()
    df.to_csv(path + "postings_same_article.csv", index=False)


def load_df_direct_comments(path="../output/") -> None:
    return pd.read_csv(path + "postings_same_article.csv")


if __name__ == '__main__':
    save_df_direct_comments()