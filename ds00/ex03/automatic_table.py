# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    automatic_table.py                                :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 23:07:01 by cmariot          #+#    #+#              #
#    Updated: 2023/10/19 22:53:40 by cmariot         ###   ########.fr        #
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


def get_files_list(directory: str) -> list[str]:
    """
    Return the list of the CSV files in the directory.
    If the directory is empty or does not contain any CSV files,
    raise a FileNotFoundError.
    """
    csv_list = []
    files_list = os.listdir(directory)
    for file in files_list:
        if file.endswith(".csv"):
            csv_list.append(file)
    if len(csv_list) == 0:
        raise FileNotFoundError(
            "The directory is empty or does not contain any CSV files."
        )
    return csv_list


def create_query(table_name: str, path: str) -> str:
    """
    Create table 'table_name' with the data from the CSV file 'path' in the
    docker container and copy the data from the CSV file to the table.
    """
    query = (
        f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name}
        (
            event_time      TIMESTAMP WITH TIME ZONE NOT NULL,
            event_type      VARCHAR(32),
            product_id      INTEGER,
            price           FLOAT,
            user_id         BIGINT,
            user_session    UUID
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

    data_dirpath_on_container = "/subject/customer/"
    filenames = get_files_list("../../subject/customer")
    table_names = [file[:-4] for file in filenames]
    file_paths = [data_dirpath_on_container + file for file in filenames]

    cursor = connection.cursor()
    for table_name, file_path in zip(table_names, file_paths):
        query: str = create_query(table_name, file_path)
        cursor.execute(query)
        connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)
