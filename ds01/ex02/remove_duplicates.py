# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    remove_duplicates.py                              :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 21:00:55 by cmariot          #+#    #+#              #
#    Updated: 2023/10/18 21:00:56 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2


# You must delete the duplicate rows in the "customers" table.
# Warning : Sometimes the server sends the same instruction
#           with 1 second interval


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
    Create a query to delete the duplicate rows in the "customers" table.
    Step 1: Create a temporary table named "tmp_customers" with the distinct
            rows of the "customers" table.
    Step 2: Truncate the "customers" table.
    Step 3: Insert the rows from the "tmp_customers" table in the "customers"
            table.
    Step 4: Drop the "tmp_customers" table.
    """

    query = (
        """
        CREATE TEMP TABLE tmp_customers AS
        (
            SELECT DISTINCT *
                FROM customers
        );

        TRUNCATE TABLE customers;

        INSERT INTO customers
        (
            SELECT * FROM tmp_customers
        );

        DROP TABLE tmp_customers;
        """
    )
    print(query)
    return query


def main():

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

    query: str = create_query()

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)

# Before: 16_536_158 rows
# After:  15_667_350 rows
