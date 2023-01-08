import itertools
import pandas as pd
import networkx as nx
import numpy as np

# Author: @peterwalchofer



def create_graph(df, article_or_ressort, user="UserCommunityName"):
    graph = nx.Graph()
    graph.add_nodes_from(df[article_or_ressort].unique())
    graph.add_nodes_from(df[user].unique())
    graph.add_edges_from(
        list(map(tuple, df[[article_or_ressort, user]].drop_duplicates().values)))
    graph = graph.to_undirected()
    return graph


def compute_overlap(graph, df, article_or_ressort, verbose=False):
    uu_overlap = {}
    article_ids = df[article_or_ressort].unique()
    for idx, article in enumerate(article_ids):
        if verbose:
            print(round((idx/len(article_ids))*100), "%", end="\r")
        users_commented = list(graph.neighbors(article))
        for uu_tuple in itertools.product(users_commented, users_commented):
            if uu_tuple[0] != uu_tuple[1]:
                if uu_tuple[0] > uu_tuple[1]:
                    uu_tuple = (uu_tuple[1], uu_tuple[0])
                if uu_tuple in uu_overlap:
                    uu_overlap[uu_tuple] += 1
                else:
                    uu_overlap[uu_tuple] = 1

    return uu_overlap


def user_lookup_df(df, article_or_ressort):
    user_num_articles = df[["UserCommunityName", article_or_ressort]].drop_duplicates()\
        .groupby(["UserCommunityName"]).size().to_frame()
    # make dict of users and the number of articles they commented on
    user_num_articles = dict(
        zip(user_num_articles.index, user_num_articles[0]))
    return user_num_articles


def compute_similarity(uu_overlap, user_num_articles, chunckIdx):
    similarities = []
    for uu_tuple in uu_overlap.keys():
        overlap = uu_overlap[uu_tuple]
        try:
            union = user_num_articles[uu_tuple[0]] + \
                user_num_articles[uu_tuple[1]]
        except:
            print(uu_tuple)
        similarities += [[uu_tuple[0], uu_tuple[1], overlap / union]]
    return pd.DataFrame(similarities, columns=["A", "B", f"Similarity_{chunckIdx}"]).set_index(["A", "B"])


def compute_time_base_similiarities(selected_postings, article_or_ressort, uu_first_contact_tuples, num_chunks=30):
    sum_sims = 0
    n = 0
    chunks = []
    running_mean = []
    for chunckIdx, subset_df in enumerate(np.array_split(selected_postings, num_chunks)):
        # print(round(chunckIdx/num_chunks) *100, " %", end="\r")
        graph_ressort = create_graph(
            subset_df, article_or_ressort, "UserCommunityName")
        uu_overlap_ressort = compute_overlap(
            graph_ressort, subset_df, article_or_ressort)
        user_num_article_or_ressort = user_lookup_df(
            subset_df, article_or_ressort)
        similarity_table_ressort = compute_similarity(
            uu_overlap_ressort, user_num_article_or_ressort, chunckIdx)

        # Filter similarity table to only include users that had frist contact in the middle.
        similarity_table_ressort_filtered = (similarity_table_ressort
                                             .merge(uu_first_contact_tuples, left_on=["A", "B"], right_on=["UserCommunityName_x", "UserCommunityName_y"], how="inner")
                                             .set_index(["UserCommunityName_x", "UserCommunityName_y"]))
        n += similarity_table_ressort_filtered.shape[0]
        sum_sims += similarity_table_ressort_filtered.sum().item()
        chunks += [similarity_table_ressort_filtered.mean()]
        running_mean += [sum_sims / n]
    return chunks, running_mean
