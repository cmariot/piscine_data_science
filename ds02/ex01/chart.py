# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    chart.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/19 17:04:38 by cmariot          #+#    #+#              #
#    Updated: 2023/10/19 17:04:39 by cmariot         ###   ########.fr        #
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
    Fetch the data from the table customers_with_duplicates.
    We need to focus only on the "purchase" data of "event_type" column.
    We need several informations to create the 3 charts:
    - The number of customers per day.
    - The total sales per mounth.
    - The average spend per customer per day.
    """

    query = (
        """
        SELECT DISTINCT
            event_time,
            user_id,
            price
        FROM customers
        WHERE event_type = 'purchase'
        ORDER BY event_time ASC;
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


def plot_customers_per_day(data: list):

    plt.title("Number of distinct customers per day")

    current_day = None
    daily_customers = []
    number_of_customers_per_day = {}

    for purchase in data:

        event_day = purchase[0].strftime("%Y-%m-%d")
        user_id = purchase[1]

        if event_day != current_day:
            current_day = event_day
            daily_customers.clear()

        if event_day not in number_of_customers_per_day:
            number_of_customers_per_day[event_day] = 1
        elif user_id not in daily_customers:
            number_of_customers_per_day[event_day] += 1
        else:
            continue

        daily_customers.append(user_id)

    x = number_of_customers_per_day.keys()
    y = number_of_customers_per_day.values()

    plt.plot(x, y)

    plt.xlabel("Date")
    plt.ylabel("Number of customers")
    plt.xticks(
        [0, 31, 61, 92, 121],
        ["Oct", "Nov", "Dec", "Jan", "Feb"]
    )
    plt.grid()
    plt.show()


def plot_sales_per_mounth(data: list):

    plt.title("Total sales per mounth in millions of Altarian Dollars (A$)")

    sales_per_mounth = {}
    for purchase in data:
        event_mounth = purchase[0].strftime("%Y-%m")
        sales = purchase[2] / 1_000_000
        if event_mounth not in sales_per_mounth:
            sales_per_mounth[event_mounth] = sales
        else:
            sales_per_mounth[event_mounth] += sales

    x = ["Oct", "Nov", "Dec", "Jan", "Feb"] if len(sales_per_mounth) == 5 \
        else sales_per_mounth.keys()
    y = sales_per_mounth.values()

    plt.bar(x, y, width=0.5)

    plt.xlabel("Mounth")
    plt.ylabel("Total sales in millions of Altarian Dollars (A$)")
    plt.grid(axis="y")
    plt.show()


def plot_average_spend_per_customer_per_day(data: list):

    plt.title("Average spend per customer per day")

    current_day = None
    customers_per_day = []
    sales_per_day = {}
    average_spend_per_customer_per_day = {}
    for purchase in data:
        event_day = purchase[0].strftime("%Y-%m-%d")
        customers_id = purchase[1]
        sales = purchase[2]

        if event_day != current_day:
            current_day = event_day
            customers_per_day.clear()
            sales_per_day[event_day] = 0
            average_spend_per_customer_per_day[event_day] = 0

        if customers_id not in customers_per_day:
            customers_per_day.append(customers_id)

        sales_per_day[event_day] += sales
        average_spend_per_customer_per_day[event_day] = \
            sales_per_day[event_day] / len(customers_per_day)

    x = average_spend_per_customer_per_day.keys()
    y = average_spend_per_customer_per_day.values()

    plt.fill_between(
        x,
        y,
        color="blue",
        alpha=0.2
    )

    plt.ylabel("Average spend per customer per day in Altarian Dollars (A$)")
    plt.ylim(0)
    plt.xlabel("Date")
    plt.xticks(
        [0, 31, 61, 92, 121],
        ["Oct", "Nov", "Dec", "Jan", "Feb"]
    )
    plt.xlim(0, 122 + 28)
    plt.grid()
    plt.show()


def main():

    data = fetch_data()

    # Data is a list of tuples.
    # Each tuple contains 3 elements:
    # - event_time
    # - user_id
    # - price

    # Plot a chart with the number of customers per day.
    plot_customers_per_day(data)

    # Plot a chart with the total sales per mounth.
    plot_sales_per_mounth(data)

    # Plot a chart with the average spend per customer per day.
    plot_average_spend_per_customer_per_day(data)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
