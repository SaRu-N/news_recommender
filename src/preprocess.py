import sys
import numpy as np
import pandas as pd
from os import path


def get_file_path(file_name):
    return path.join(DATA_PATH, file_name)


def preprocess_data():
    users_df = pd.read_csv(get_file_path("users.csv"))
    news_df = pd.read_csv(get_file_path("news.csv"))
    ratings_df = pd.read_csv(get_file_path("ratings.csv"))
    likes_df = pd.read_csv(get_file_path("likes.csv"))

    print(news_df.head())

    # add an id column beginning from 0
    users_df["user_id"] = [i for i in range(users_df.shape[0])]
    news_df["news_id"] = [i for i in range(news_df.shape[0])]

    # Count the ratings by deleted users
    sum = 0
    for i, x in enumerate(ratings_df["User"]):
        if len(users_df[users_df.User == x].index) != 1:
            # print(f"user {x} in of {i}th row")
            sum += 1
    print(f"Total ratings to discard {sum}")

    # remove user ratings associated to deleted users
    ratings_df = ratings_df[ratings_df.User.isin(users_df.User)]

    # map user id to the index of the user in user table
    ratings_df["news_id"] = ratings_df["News"].apply(
        lambda x: news_df[news_df.Id == x].index[0]
    )

    # map news id to the index of the news table
    ratings_df["user_id"] = ratings_df["User"].apply(
        lambda x: users_df[users_df.User == x].index[0]
    )


if __name__ == "__main__":
    print("Hello World!")
    DATA_PATH = path.abspath(sys.argv[1])
    # data_root = 'data/'
    preprocess_data()
