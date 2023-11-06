# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    points.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/11/06 16:48:28 by cmariot          #+#    #+#              #
#    Updated: 2023/11/06 16:48:35 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


import matplotlib.pyplot as plt
import pandas


def train_separate(axes, dataset_train, separated_features):
    jedi = dataset_train[dataset_train["knight"] == "Jedi"]
    axes[0, 0].scatter(
        jedi[separated_features[0]],
        jedi[separated_features[1]],
        c="red",
        label="Jedi",
        alpha=0.5
    )
    sith = dataset_train[dataset_train["knight"] == "Sith"]
    axes[0, 0].scatter(
        sith[separated_features[0]],
        sith[separated_features[1]],
        c="blue",
        label="Sith",
        alpha=0.5
    )
    axes[0, 0].set_title("Train dataset", fontsize=12)
    axes[0, 0].set_xlabel(separated_features[0], fontsize=10)
    axes[0, 0].set_ylabel(separated_features[1], fontsize=10)
    axes[0, 0].legend(loc="upper left", fontsize=10)
    return axes


def test_separate(axes, dataset_test, separated_features):
    axes[1, 0].scatter(
        dataset_test[separated_features[0]],
        dataset_test[separated_features[1]],
        c="green",
        label="Knight",
        alpha=0.5
    )
    axes[1, 0].set_title("Test dataset", fontsize=12)
    axes[1, 0].set_xlabel(separated_features[0], fontsize=10)
    axes[1, 0].set_ylabel(separated_features[1], fontsize=10)
    axes[1, 0].legend(loc="upper left", fontsize=10)
    return axes


def train_mix(axes, dataset_train, mix_features):
    jedi = dataset_train[dataset_train["knight"] == "Jedi"]
    axes[0, 1].scatter(
        jedi[mix_features[0]],
        jedi[mix_features[1]],
        c="red",
        label="Jedi",
        alpha=0.5
    )
    sith = dataset_train[dataset_train["knight"] == "Sith"]
    axes[0, 1].scatter(
        sith[mix_features[0]],
        sith[mix_features[1]],
        c="blue",
        label="Sith",
        alpha=0.5
    )
    axes[0, 1].set_title("Train dataset", fontsize=12)
    axes[0, 1].set_xlabel(mix_features[0], fontsize=10)
    axes[0, 1].set_ylabel(mix_features[1], fontsize=10)
    axes[0, 1].legend(loc="upper right", fontsize=10)
    return axes


def test_mix(axes, dataset_test, mix_features):
    axes[1, 1].scatter(
        dataset_test[mix_features[0]],
        dataset_test[mix_features[1]],
        c="green",
        label="Knight",
        alpha=0.5
    )
    axes[1, 1].set_title("Test dataset", fontsize=12)
    axes[1, 1].set_xlabel(mix_features[0], fontsize=10)
    axes[1, 1].set_ylabel(mix_features[1], fontsize=10)
    axes[1, 1].legend(loc="upper right", fontsize=10)
    return axes


def main():

    # Read the datasets.
    dataset_train = pandas.read_csv("../Train_knight.csv")
    dataset_test = pandas.read_csv("../Test_knight.csv")

    fig, axes = plt.subplots(2, 2, figsize=(15, 9))

    fig.suptitle("Points of the features for the Train and Test datasets")

    separated_features = ["Empowered", "Stims"]
    axes = train_separate(axes, dataset_train, separated_features)
    axes = test_separate(axes, dataset_test, separated_features)

    mix_features = ["Push", "Deflection"]
    axes = train_mix(axes, dataset_train, mix_features)
    axes = test_mix(axes, dataset_test, mix_features)

    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
