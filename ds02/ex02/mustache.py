# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    mustache.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/20 12:29:07 by cmariot          #+#    #+#              #
#    Updated: 2023/10/20 12:29:08 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2
import pandas
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


def create_query_1() -> str:

    query = (
        """
        SELECT DISTINCT
            event_time,
            price,
            user_id
        FROM customers
            WHERE event_type = 'purchase' AND event_time < '2023-02-01';
        """
    )
    print(query)
    return query


def create_query_2() -> str:

    query = (
        """
        WITH basket_prices AS (
            SELECT
                user_id,
                SUM(price) AS purchase_prices
            FROM
                customers
            WHERE
                event_type = 'purchase'
                AND event_time < '2023-02-01'
                AND price > 0
            GROUP BY
                user_id, event_time
            ORDER BY
                user_id ASC
        ),
        average_basket_prices AS (
            SELECT
                user_id,
                AVG(purchase_prices) AS avg_basket_price
            FROM
                basket_prices
            GROUP BY
                user_id
        )
        SELECT
            user_id,
            avg_basket_price
        FROM
            average_basket_prices;

        """
    )
    print(query)
    return query


def fetch_data(index: int) -> list:
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

    query = {
        1: create_query_1,
        2: create_query_2
    }

    cursor = connection.cursor()
    cursor.execute(query[index]())
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return data


def box_plot_with_outliers(dataframe: pandas.DataFrame) -> None:
    """
    Create a box plot with outliers.
    """
    plt.title("Price distribution")
    plt.boxplot(
        x=dataframe,            # Array to be plotted.
        vert=False,             # Vertical or horizontal.
        patch_artist=True,      # Fill with color.
        showfliers=True,        # Show the outliers.
        labels=["Purchase"],    # Tick labels.
        autorange=True,         # Automatic range.
        flierprops=dict(
            markerfacecolor='black',
            marker='D',
            markersize=2,
        ),
    )
    plt.grid(True, axis='x')
    plt.xlabel("Price in A$")
    plt.show()


def box_plot_without_outliers(dataframe: pandas.DataFrame) -> None:
    """
    Create a box plot without outliers.
    """
    plt.title("Price distribution without outliers")
    plt.boxplot(
        x=dataframe,            # Array to be plotted.
        vert=False,             # Vertical or horizontal.
        patch_artist=True,      # Fill with color.
        showfliers=False,       # Show the outliers.
        labels=["Purchase"],    # Tick labels.
        autorange=True,         # Automatic range.
    )
    plt.grid(True, axis='x')
    plt.xlabel("Price in A$")
    plt.show()


def box_plot_avg(dataframe: pandas.DataFrame) -> None:
    """
    Create a box plot without outliers.
    """

    plt.title("Average basket price per user")
    plt.boxplot(
        x=dataframe["avg"],     # Array to be plotted.
        vert=False,             # Vertical or horizontal.
        patch_artist=True,      # Fill with color.
        showfliers=False,       # Show the outliers.
        labels=["Purchase"],    # Tick labels.
        autorange=True,         # Automatic range.
    )
    plt.show()


def main():

    data = fetch_data(1)

    complete_df = pandas.DataFrame(
        data,
        columns=['event_time', 'price', 'user_id']
    )

    dataframe = complete_df["price"]
    print(dataframe.describe())

    box_plot_with_outliers(dataframe)

    box_plot_without_outliers(dataframe)

    # wtf w/ the subject last plot ?

    data = fetch_data(2)

    dataframe = pandas.DataFrame(
        data,
        columns=['id', 'avg']
    )

    box_plot_avg(dataframe)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)


# Act like my data analyst assistant.

# I want to plot a box plot of the average basket_price per customer.
# My data is stored in a postgresql database,
# the customers table has different columns :
# - event_time : date of the event
# - event_type : type of event (view, cart, remove from cart, purchase)
# - product_id : id of the product assiociated with the event
# - price : price of ONE product associated with an event
# - user_id : id of the user who made the action
# - user_session : uuid of the user session

# Makes a Postgresql query to get the average basket_price per customer with
# the customers table.
# First you must you must compute the basket price based on the price of the
# products associated with the purchase events.
# Then you must compute the average basket price per customer.
