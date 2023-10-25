# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    elbow.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/23 17:35:45 by cmariot          #+#    #+#              #
#    Updated: 2023/10/23 17:35:46 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

# Use of the elbow method to find the optimal number of clusters for
# the k-means algorithm.

import os
from dotenv import load_dotenv
import psycopg2
import pandas
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


def load_env(dotenv_path: str) -> tuple:
    """
    Load the postgresql config from the .env_postgres file.
    Return a tuple with the config.
    """
    env_file_loaded = load_dotenv(dotenv_path)
    if env_file_loaded is False:
        raise FileNotFoundError(
            "The .env_postgres file is missing or is empty."
        )
    environment_variables = (
        os.getenv('POSTGRES_HOST'),
        os.getenv('POSTGRES_DB'),
        os.getenv('POSTGRES_USER'),
        os.getenv('POSTGRES_PASSWORD'),
        os.getenv('POSTGRES_PORT')
    )
    if any(variable is None for variable in environment_variables):
        raise ValueError(
            "One or more config variables are missing.\n" +
            "Please check the .env_postgres file."
        )
    return environment_variables


def create_query() -> str:

    query = (
        """
        SELECT * FROM customers;
        """
    )
    print(query)
    return query


def fetch_data() -> list:
    (host, database, username, password, port) = load_env(
        "../../postgresql_docker/.env_postgres"
    )

    connection = psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=password,
        port=port
    )

    query = create_query()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def main():

    data = fetch_data()

    customers = pandas.DataFrame(
        data,
        columns=[
            "event_time",
            "event_type",
            "product_id",
            "price",
            "user_id",
            "user_session"
        ]
    )

    print(customers.head())

    inertia = []
    max_clusters = 10
    for n_clusters in range(1, max_clusters):

        print(f"Clustering step {n_clusters}/{max_clusters}")

        kmean = KMeans(
            n_clusters=n_clusters,
            max_iter=1000,

        )
        kmean.fit(customers)
        inertia.append(kmean.inertia_)

    # Plot the inertia depending on the number of clusters
    # to find the optimal number of clusters
    # Elbow method

    plt.plot(range(1, max_clusters), inertia)
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)