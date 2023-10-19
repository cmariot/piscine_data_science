# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    fusion.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/19 12:13:38 by cmariot          #+#    #+#              #
#    Updated: 2023/10/19 12:13:43 by cmariot         ###   ########.fr        #
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


def create_query() -> str:

    query = (
        """
        ALTER TABLE customers
            ADD COLUMN category_id    BIGINT,
            ADD COLUMN category_code  VARCHAR(255),
            ADD COLUMN brand          VARCHAR(255);

        UPDATE customers
            SET
                category_id = tmp_items.category_id,
                category_code = tmp_items.category_code,
                brand = tmp_items.brand
            FROM (
                SELECT
                    product_id,
                    COALESCE(MAX(category_id), NULL) AS category_id,
                    COALESCE(MAX(category_code), NULL) AS category_code,
                    COALESCE(MAX(brand), NULL) AS brand
                FROM items GROUP BY product_id
            ) AS tmp_items
            WHERE customers.product_id = tmp_items.product_id;
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
