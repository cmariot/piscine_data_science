# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    customers_table.py                                :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 18:36:35 by cmariot          #+#    #+#              #
#    Updated: 2023/10/18 18:36:36 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2


# You have to join all the data_202*_*** tables together
# in a table called "customers"


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
            f"Please check the {dotenv_path} file."
        )
    return environment_variables


def match_pattern(table_name: str) -> bool:
    """
    Return True if the table name matches the pattern data_202*_***.
    """
    if (
        table_name.startswith("data_202")
        and len(table_name) == len("data_202*_***")
        and table_name[-4] == "_"
    ):
        return True
    else:
        return False


def create_query(cursor: psycopg2.extensions.cursor) -> str:
    """
    Create a query to create a table named "customers" with all the data
    from the tables matching the pattern data_202*_***.
    """

    # Retrieve the table names from the database.
    cursor.execute(
        """
        SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
    )
    database_table_names = cursor.fetchall()
    if len(database_table_names) == 0:
        raise ValueError("The database is empty.")

    # Filter the table names to keep only the ones matching the pattern.
    table_names = [
        table[0] for table in database_table_names
        if match_pattern(table[0])
    ]
    if len(table_names) == 0:
        raise ValueError("There are no tables matching the pattern.")

    select_statement = (
        """
        )
        UNION ALL
        (
            """.join(
            [f"SELECT * FROM {table_name} " for table_name in table_names]
        )
    )

    query = (
        f"""
        DROP TABLE IF EXISTS customers;
        CREATE TABLE customers AS
        (
            {select_statement}
        );
        """
    )

    print(query)

    # The query looks like this:

    # DROP TABLE IF EXISTS customers;
    # CREATE TABLE IF NOT EXISTS customers AS
    # (
    #     SELECT * FROM data_2022_oct
    # )
    # UNION ALL
    # (
    #     SELECT * FROM data_2022_nov
    # )
    # UNION ALL
    # (
    #     SELECT * FROM data_2023_jan
    # )
    # UNION ALL
    # (
    #     SELECT * FROM data_2022_dec
    # );

    # UNION ALL is faster than UNION because it does not remove duplicates.

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

    cursor = connection.cursor()
    query: str = create_query(cursor)
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)


