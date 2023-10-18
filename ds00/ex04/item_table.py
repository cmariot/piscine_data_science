# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    item_table.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/18 17:36:36 by cmariot          #+#    #+#              #
#    Updated: 2023/10/18 17:36:40 by cmariot         ###   ########.fr        #
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


def main():

    (host, database, username, password, port) = load_env(
        "../postgresql_docker/.env_postgres"
    )

    directory_path = "../data/item"
    csv_name = "item.csv"
    file_path = os.path.join(directory_path, csv_name)

    if csv_name.endswith(".csv") is False:
        raise ValueError("The file name is not a CSV file.")

    file_data = pandas.read_csv(file_path)
    table_name = csv_name[:-4]
    table_dtype = {
        "product_id": sqlalchemy.Integer,
        "category_id": sqlalchemy.BigInteger,
        "category_code": sqlalchemy.String,
        "brand": sqlalchemy.String,
    }

    engine = sqlalchemy.create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}",
        echo=True,
    )

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
