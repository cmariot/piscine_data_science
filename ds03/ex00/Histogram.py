# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    Histogram.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/11/06 15:39:11 by cmariot          #+#    #+#              #
#    Updated: 2023/11/06 16:04:20 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pandas
import matplotlib.pyplot as plt


def plot_train_histograms(dataset):
    sith = dataset[dataset["knight"] == "Sith"]
    jedi = dataset[dataset["knight"] == "Jedi"]
    # Drop the "knight" column.
    dataset = dataset.drop(columns=["knight"])
    # Plot the histograms.
    fig, axes = plt.subplots(6, 5, figsize=(15, 9))
    fig.suptitle("Histogram of the features for the Train dataset",
                 fontsize=16)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    i = j = 0
    for feature in dataset.columns:
        axes[i][j].hist(sith[feature], bins=42, alpha=0.5, color="red")
        axes[i][j].hist(jedi[feature], bins=42, alpha=0.5, color="blue")
        axes[i][j].set_title(feature, fontsize=10)
        i += 1 if j == 4 else 0
        j = 0 if j == 4 else j + 1
    plt.show()


def plot_test_histograms(dataset):
    fig, axes = plt.subplots(6, 5, figsize=(15, 9))
    fig.suptitle("Histogram of the features for the Test dataset", fontsize=16)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    i = j = 0
    for feature in dataset.columns:
        axes[i][j].hist(dataset[feature], bins=42, alpha=0.5, color="green")
        axes[i][j].set_title(feature, fontsize=10)
        i += 1 if j == 4 else 0
        j = 0 if j == 4 else j + 1
    plt.show()


def main():
    dataset_test = pandas.read_csv("../Test_knight.csv")
    plot_test_histograms(dataset_test)
    dataset_train = pandas.read_csv("../Train_knight.csv")
    plot_train_histograms(dataset_train)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
