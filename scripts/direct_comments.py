import pandas as pd

from load_data import load_postings


def create_df_direct_comments() -> pd.DataFrame:
    postings = load_postings()

    merged = pd.merge(postings, postings, left_on="ID_Posting", right_on="ID_Posting_Parent")

    filtered = merged[merged["UserCommunityName_x"] != merged["UserCommunityName_y"]]

    filtered.rename(columns={"UserCommunityName_x": "UserPost",
                             "UserCommunityName_y": "UserComment",
                             "ID_Posting_x": "ID_Posting",
                             "ID_Posting_y": "ID_Posting_Comment",
                             "PostingCreatedAt_y": "CommentCreatedAt"}, inplace=True)

    return filtered[["UserPost", "UserComment", "ID_Posting", "ID_Posting_Comment", "CommentCreatedAt"]]


def save_df_direct_comments(path="../output/") -> None:
    df = create_df_direct_comments()
    df.to_csv(path + "direct_comments.csv", index=False)


def load_df_direct_comments(path="../output/") -> None:
    return pd.read_csv(path + "direct_comments.csv")


if __name__ == '__main__':
    save_df_direct_comments()
