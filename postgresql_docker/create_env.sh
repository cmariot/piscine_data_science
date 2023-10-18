#!/bin/bash

# Create a .env_postgres file with the following variables :
# - POSTGRES_USER
# - POSTGRES_PASSWORD
# - POSTGRES_DB

# Create a .env_pgadmin file with the following variables :
# - PGADMIN_DEFAULT_EMAIL
# - PGADMIN_DEFAULT_PASSWORD

# The variables will be prompted to the user


create_postgres_env() {
    read -p "Enter the postgres user: " POSTGRES_USER
    read -p "Enter the postgres password: " POSTGRES_PASSWORD
    read -p "Enter the postgres database: " POSTGRES_DB
    echo "POSTGRES_USER=$POSTGRES_USER" > .env_postgres
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env_postgres
    echo "POSTGRES_DB=$POSTGRES_DB" >> .env_postgres
    echo "POSTGRES_HOST='localhost'" >> .env_postgres
    echo "POSTGRES_PORT=5432" >> .env_postgres
}

create_pgadmin_env() {
    read -p "Enter the pgadmin email: " PGADMIN_DEFAULT_EMAIL
    read -p "Enter the pgadmin password: " PGADMIN_DEFAULT_PASSWORD
    echo "PGADMIN_DEFAULT_EMAIL=$PGADMIN_DEFAULT_EMAIL" > .env_pgadmin
    echo "PGADMIN_DEFAULT_PASSWORD=$PGADMIN_DEFAULT_PASSWORD" >> .env_pgadmin
}

main() {
    create_postgres_env
    create_pgadmin_env
}

main