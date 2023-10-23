# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    pie.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/19 16:34:40 by cmariot          #+#    #+#              #
#    Updated: 2023/10/19 16:34:41 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt


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
    Query to get the usefull data to create the pie-chart from the database.
    We want to know the proportion of each category of event_types in the
    customers table.
    """

    query = (
        """
        SELECT
            event_type,
            COUNT(event_type) AS count
        FROM customers
        GROUP BY event_type
        ORDER BY count DESC;
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

    print("Data fetched from the database:", data)
    return data


def pie_plot(data: list) -> None:

    event_types = [event_type for event_type, count in data]
    event_count = [count for event_type, count in data]

    plt.title(
        "Proportion of each category of event_types in the customers table"
    )

    plt.pie(
        x=event_count,
        labels=event_types,
        autopct='%1.1f%%',
    )

    plt.show()


def main():
    data = fetch_data()
    pie_plot(data)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
