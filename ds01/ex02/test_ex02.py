# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test_ex02.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 19:19:05 by cmariot          #+#    #+#              #
#    Updated: 2023/10/28 19:19:06 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import os
import pandas
import sqlalchemy
from dotenv import load_dotenv


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


def get_customers() -> pandas.DataFrame:
    """
    Return all the rows in the "customers" table.
    """
    print("Loading customers table...")

    csv_path = "customers.csv"

    # If the csv file already exists, load it.
    if os.path.isfile(csv_path):
        customers = pandas.read_csv(csv_path)
        return customers

    # Else load the "customers" table from the postgresql database.
    (host, database, username, password, port) = load_env(
        "../../postgresql_docker/.env_postgres"
    )
    connection = sqlalchemy.create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}"
    )
    customers = pandas.DataFrame()
    for chunk in pandas.read_sql_table(
        "customers",
        connection,
        chunksize=1_000_000
    ):
        customers = pandas.concat([customers, chunk])
        print("1_000_000 lines loaded in the Dataframe...")
    customers.to_csv(csv_path, index=False)
    connection.dispose()
    return customers


def main():

    customers = get_customers()

    print(
        "Original customers table :\n",
        customers,
        "\n\n"
    )

    duplicates = customers[customers.duplicated()]

    print(
        "Duplicate rows in the customers table :\n",
        duplicates.to_string(index=False),
        "\n\n"
    )

    # Drop the duplicate rows in the "customers" table.
    customers.drop_duplicates(
        subset=[
            'event_time',
            'event_type',
            'product_id',
            'price',
            'user_id',
            'user_session'
        ],
        keep='first',
        inplace=True
    )

    customers.sort_values(
        by=["event_time", "user_id"],
        inplace=True
    )

    print(
        "Customers table without duplicates :\n",
        customers,
        "\n\n"
    )

    duplicates = customers[customers.duplicated()]

    print(
        "Duplicate rows in the customers table after remove_duplicates :\n",
        duplicates.to_string(index=False),
        "\n\n"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error:", error)


# Tests pour essayer d'obtenir 18_525_251 lignes :

# Table customers : 20_692_840 lignes (avec les doublons, ok)
# After remove_duplicates, customers table should have 18_525_251 lines.

# ............................

# 1) Essais en conservant 1 ligne parmi les lignes en double
#    (si il y a des lignes dupliquées, on en garde une) :

#  Supprimer les lignes en double en prenant en compte toutes les colonnes :
#  19_583_742 lignes

#  Supprimer les lignes en double en prenant en compte toutes les colonnes sauf
#  la colonne "event_time" :
#  17_062_104 lignes

#  Supprimer les lignes en double en prenant en compte toutes les colonnes sauf
#  la colonne "user_session" :
#  19_571_891 lignes

#  Supprimer les lignes en double en prenant en compte toutes les colonnes sauf
#  la colonne "price" :
#  19_583_742 lignes
#  -> Prix fixe pour chaque produit.

#  Les autres colonnes me semblent importantes pour identifier une action.

# ............................

# 2) Essais en ne conservant AUCUNE ligne parmi les lignes en double,
#    si il y a des doublons on les supprime :

#  Supprimer les lignes en double en prenant en compte toutes les colonnes :
#  18_537_980 lignes

#  Supprimer les lignes en double en prenant en compte toutes les colonnes sauf
#  la colonne "event_time" :
#  14_439_882 lignes

#  Supprimer les lignes en double en prenant en compte toutes les colonnes sauf
#  la colonne "user_session" :
#  18_517_940 lignes

# ..............................

# Drop the rows with missing values.
# customers.dropna(inplace=True)

# # Remove the lines with product_id that are not in the "items" table.
# items = pandas.read_sql_table("items", connection)
# items = items['product_id'].unique()
# customers = customers[customers['product_id'].isin(items)]

# ..............................

# Conclusion :
# L'objectif est de supprimer les lignes dupliquees dans la table customers.
# Je vais supprimer les lignes dupliquees en prenant en compte
# toutes les colonnes et conserver une ligne parmi les doublons.

# Le nombre de lignes dans la table customers sans doublons est de 19_583_742.

# SELECT   COUNT(*) AS nb_doublon,
#          event_time,
#          user_id,
#          user_session,
#          product_id,
#          price,
#          event_type
# FROM     customers
# GROUP BY event_time,
#          user_id,
#          user_session,
#          product_id,
#          price,
#          event_type
# HAVING COUNT(*) > 1

# -> plus de doublons, mais un nombre de lignes different de 18_525_251 attendu

# SELECT *
# FROM customers
# WHERE event_time = '2023-02-28 23:42:29+00:00'
#     AND event_type ='remove_from_cart'
#     AND product_id = '5692888'
#     AND price = '7.29'
#     AND user_id = '548866558'
#     AND user_session = '199869f5-3a22-4a47-8678-7c343d09bb8e'
