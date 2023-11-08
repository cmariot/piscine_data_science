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
import matplotlib.pyplot as plt


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


def train_separate(axes, dataset_train, separated_features):
    jedi = dataset_train[dataset_train["knight"] == "Jedi"]
    axes[0].scatter(
        jedi[separated_features[0]],
        jedi[separated_features[1]],
        c="red",
        label="Jedi",
        alpha=0.5
    )
    sith = dataset_train[dataset_train["knight"] == "Sith"]
    axes[0].scatter(
        sith[separated_features[0]],
        sith[separated_features[1]],
        c="blue",
        label="Sith",
        alpha=0.5
    )
    axes[0].set_title("Train dataset", fontsize=12)
    axes[0].set_xlabel(separated_features[0], fontsize=10)
    axes[0].set_ylabel(separated_features[1], fontsize=10)
    axes[0].legend(loc="upper left", fontsize=10)
    return axes


def test_separate(axes, dataset_test, separated_features):
    axes[1].scatter(
        dataset_test[separated_features[0]],
        dataset_test[separated_features[1]],
        c="green",
        label="Knight",
        alpha=0.5
    )
    axes[1].set_title("Test dataset", fontsize=12)
    axes[1].set_xlabel(separated_features[0], fontsize=10)
    axes[1].set_ylabel(separated_features[1], fontsize=10)
    axes[1].legend(loc="upper left", fontsize=10)
    return axes


def main():

    # Read the datasets.
    dataset_train = pandas.read_csv("../Train_knight.csv")
    dataset_test = pandas.read_csv("../Test_knight.csv")

    # Standardize the datasets.
    dataset_train_standardized = standardize(dataset_train)
    dataset_test_standardized = standardize(dataset_test)

    print(dataset_train_standardized)
    print(dataset_test_standardized)

    fig, axes = plt.subplots(2, figsize=(10, 9))

    fig.suptitle("Points of the features for the Train and Test datasets")

    separated_features = ["Empowered", "Stims"]
    axes = train_separate(axes, dataset_train_standardized, separated_features)
    axes = test_separate(axes, dataset_test_standardized, separated_features)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
