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
        SELECT
            COUNT(user_id) AS nb_orders,
            SUM(price) AS total_spent,
            AVG(price) AS avg_spent,
            MIN(price) AS min_spent,
            MAX(price) AS max_spent
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id;
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
            'nb_orders',
            'total_spent',
            'avg_spent',
            'min_spent',
            'max_spent'
        ]
    )

    print(customers.head(), "\n")

    # Inertia can be recognized as a measure of how internally coherent
    # clusters are.
    inertia = []
    max_clusters = 10
    for n_clusters in range(1, max_clusters + 1):

        print(f"Clustering step {n_clusters}/{max_clusters}")

        kmean = KMeans(
            n_clusters=n_clusters,
            max_iter=1000,
            n_init=10,
        )
        kmean.fit(customers)
        inertia.append(kmean.inertia_)

        # Plot the data with the clusters with a 3D graph
        # ax = plt.figure().add_subplot(projection='3d')
        # ax.scatter(
        #     customers['nb_orders'],
        #     customers['total_spent'],
        #     customers['avg_spent'],
        #     c=kmean.labels_
        # )
        # plt.show()

    # Plot the inertia depending on the number of clusters
    # to find the optimal number of clusters
    plt.title("Inertia depending on the number of clusters")
    plt.plot(
        range(1, max_clusters + 1),
        inertia
    )
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
