# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    items_table.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 17:36:36 by cmariot          #+#    #+#              #
#    Updated: 2023/10/19 23:13:31 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
from dotenv import load_dotenv
import psycopg2


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


def create_query(table_name: str, path: str) -> str:
    """
    Create table 'table_name' with the data from the CSV file 'path' in the
    docker container and copy the data from the CSV file to the table.
    """
    query = (
        f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        (
            product_id      INTEGER,
            category_id     BIGINT,
            category_code   VARCHAR(255),
            brand           VARCHAR(255)
        );
        COPY {table_name} FROM '{path}' DELIMITER ',' CSV HEADER;
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

    cursor = connection.cursor()
    query: str = create_query(
        table_name="items",
        path="/subject/item/item.csv"
    )
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
