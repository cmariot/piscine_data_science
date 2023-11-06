# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    standardization.py                                :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/11/06 18:08:35 by cmariot          #+#    #+#              #
#    Updated: 2023/11/06 18:08:36 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pandas


def standardize(dataset):
    """
    Standardize the dataset.
    """
    for feature in dataset.columns:
        if dataset[feature].dtype != "object":
            dataset[feature] = (
                dataset[feature] - dataset[feature].mean()
            ) / dataset[feature].std()
    return dataset


def main():

    # Read the datasets.
    dataset_train = pandas.read_csv("../Train_knight.csv")
    dataset_test = pandas.read_csv("../Test_knight.csv")

    # Standardize the datasets.
    dataset_train_standardized = standardize(dataset_train)
    dataset_test_standardized = standardize(dataset_test)

    print(dataset_train_standardized)
    print(dataset_test_standardized)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
