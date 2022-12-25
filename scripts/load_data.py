import pandas as pd


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
