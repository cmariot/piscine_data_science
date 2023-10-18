# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    automatic_table.py                                :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 17:27:22 by cmariot          #+#    #+#              #
#    Updated: 2023/10/18 17:27:23 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
import pandas
from dotenv import load_dotenv
import sqlalchemy


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


def main():

    (host, database, username, password, port) = load_env(
        "../postgresql_docker/.env_postgres"
    )

    directory_path = "../data/customer"
    csv_names_list = get_files_list(directory_path)

    table_dtype = {
        "event_time": sqlalchemy.DateTime,
        "event_type": sqlalchemy.String,
        "product_id": sqlalchemy.Integer,
        "price": sqlalchemy.Float,
        "user_id": sqlalchemy.BigInteger,
        "user_session": sqlalchemy.Uuid,
    }

    engine = sqlalchemy.create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}",
        echo=True,
    )

    for csv_name in csv_names_list:

        if csv_name.endswith(".csv") is False:
            raise ValueError("The file name is not a CSV file.")

        file_path = os.path.join(directory_path, csv_name)
        file_data = pandas.read_csv(file_path)
        table_name = csv_name[:-4]

        file_data.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            dtype=table_dtype,
        )

    engine.dispose()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
