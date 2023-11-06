# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    Clustering.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/11/02 14:24:28 by cmariot          #+#    #+#              #
#    Updated: 2023/11/02 14:24:29 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

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
    """
    Your boss wants to make groups of type of customer to make a commercial
    targeting with offers by e-mails
    (welcome offers for new customers, coupon to bring back old customers,
    special status for loyal customers like: gold, silver, platinum ...)

    Make at least 4 groups (new customer, inactive customer, loyalty status:
    gold + silver + platinum ...)

    Clustering will be based on:
    - Median frequency of purchase : number of days between two purchases
    - Median recency of purchase : number of days since the last purchase
    """

    query = (
        """
        SELECT
            user_id,
            event_time,
            price
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY
            user_id,
            event_time,
            price
        ORDER BY user_id;
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
            "user_id",
            "event_time",
            "price"
        ]
    )

    print(customers, "\n")

    # Create a new dataframe grouped by user_id and with :

    # Convert event_time into an integer, the minimum value is 0, each day is 1
    max_date = customers["event_time"].max()
    customers["event_time"] = customers["event_time"].apply(
        lambda x: (max_date - x).days + 1
    )

    customers = customers.groupby("user_id")

    customers = customers.agg(
        recency=("event_time", "min"),
        frequency=("event_time", "count"),
        monetary=("price", "sum")
    )

    # Clustering
    # K-means algorithm
    KMeans_model = KMeans(n_clusters=5, n_init=10, max_iter=5_000)
    KMeans_model.fit(customers)
    customers["cluster"] = KMeans_model.predict(customers)

    status = [
        "New customer",
        "Inactive customer",
        "Silver customer",
        "Gold customer",
        "Platinum customer"
    ]

    customers["status"] = customers["cluster"].apply(
        lambda x: status[x]
    )

    fig, ax = plt.subplots(1, 3, figsize=(20, 6))

    fig.suptitle("Customers clustering")

    ax[0].scatter(
        customers["recency"],
        customers["frequency"],
        c=customers["cluster"],
        alpha=0.25
    )
    # Plot the centroids
    ax[0].scatter(
        KMeans_model.cluster_centers_[:, 0],
        KMeans_model.cluster_centers_[:, 1],
        c='red',
        s=50,
        alpha=0.5
    )

    ax[0].set_xlabel("Recency")
    ax[0].set_ylabel("Frequency")

    ax[1].scatter(
        customers["frequency"],
        customers["monetary"],
        c=customers["cluster"],
        alpha=0.25
    )
    # Plot the centroids
    ax[1].scatter(
        KMeans_model.cluster_centers_[:, 1],
        KMeans_model.cluster_centers_[:, 2],
        c='red',
        s=50,
        alpha=0.5
    )
    ax[1].set_xlabel("Frequency")
    ax[1].set_ylabel("Monetary")

    ax[2].scatter(
        customers["monetary"],
        customers["recency"],
        c=customers["cluster"],
        alpha=0.25,
    )
    # Plot the centroids
    ax[2].scatter(
        KMeans_model.cluster_centers_[:, 2],
        KMeans_model.cluster_centers_[:, 0],
        c='red',
        s=50,
        alpha=0.5
    )
    ax[2].set_xlabel("Monetary")
    ax[2].set_ylabel("Recency")

    # Sort the clusters
    # cluster 0: New customer
    # (smallest recency, smallest frequency, smallest monetary)
    # cluster 1: Inactive customer
    # (biggest recency, smallest frequency, smallest monetary)
    # cluster 2: Silver customer
    # (biggest recency, biggest frequency, smallest monetary)
    # cluster 3: Gold customer
    # (biggest recency, biggest frequency, biggest monetary)
    # cluster 4: Platinum customer
    # (biggest spenders)

    # Add labels
    for i, txt in enumerate(status):
        ax[0].annotate(
            txt,
            (KMeans_model.cluster_centers_[i, 0],
             KMeans_model.cluster_centers_[i, 1])
        )
        ax[1].annotate(
            txt,
            (KMeans_model.cluster_centers_[i, 1],
             KMeans_model.cluster_centers_[i, 2])
        )
        ax[2].annotate(
            txt,
            (KMeans_model.cluster_centers_[i, 2],
             KMeans_model.cluster_centers_[i, 0])
        )

    plt.show()

    plt.pie(
        customers["cluster"].value_counts(),
        labels=customers["cluster"].value_counts().index,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )
    plt.legend()
    plt.title("Customers clustering")
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
