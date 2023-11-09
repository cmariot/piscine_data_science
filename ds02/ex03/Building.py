# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    Building.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/22 11:43:25 by cmariot          #+#    #+#              #
#    Updated: 2023/10/22 11:43:27 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import pandas


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


def create_query_1() -> str:
    """
    """

    query = (
        """
            SELECT
                user_id,
                COUNT(*) AS frequency
            FROM
                customers
            WHERE
                event_type = 'purchase'
            GROUP BY
                user_id
            HAVING
                COUNT(*) < 40
            ORDER BY
                COUNT(*) ASC;
        """
    )
    print(query)
    return query


def create_query_2() -> str:
    """
    """

    query = (
        """
            SELECT
                user_id,
                SUM(price) AS spent
            FROM
                customers
            WHERE
                event_type = 'purchase'
            GROUP BY
                user_id
            HAVING
                SUM(price) < 225
            ORDER BY
                SUM(price) ASC;
        """
    )
    print(query)
    return query


def fetch_data(querry_number: int) -> list:
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

    querries = {
        1: create_query_1,
        2: create_query_2
    }

    query = querries[querry_number]()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def main():

    data = fetch_data(1)
    dataframe = pandas.DataFrame(data, columns=['id', 'frequency'])

    # Plot a bar chart with the number of orders per customer distribution
    plt.title("Frequency distribution of the number of orders per customer")
    plt.hist(dataframe['frequency'], bins=5, edgecolor='white')
    plt.xlabel("Number of orders")
    plt.ylabel("Count of customers")
    plt.grid(alpha=0.75)
    plt.show()

    data = fetch_data(2)
    dataframe = pandas.DataFrame(data, columns=['id', 'frequency'])

    # Plot a bar chart with the $ spent per user distribution
    plt.title("Frequency distribution of the purchase prices per customer")
    plt.hist(dataframe['frequency'], bins=5, edgecolor='white')
    plt.xlabel("Monetary value in Altairian Dollars (A$)")
    plt.ylabel("Count of customers")
    plt.grid(alpha=0.75)
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
