# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    Correlation.py                                    :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: cmariot <cmariot@student.42.fr>           +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2023/11/06 16:05:17 by cmariot          #+#    #+#              #
#    Updated: 2023/11/06 16:19:58 by cmariot         ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pandas


def correlation_factor(serie, target):
    """
    Calculate the correlation between a serie and a target.
    """
    covariance = serie.cov(target)
    serie_std = serie.std()
    target_std = target.std()
    if serie_std != 0 and target_std != 0:
        correlation = covariance / (serie_std * target_std)
    else:
        correlation = 0
    return abs(correlation)


def main():

    # Read the dataset.
    dataset_train = pandas.read_csv("../Train_knight.csv")

    # Convert the "knight" column to numerical values.
    dataset_train["knight"] = dataset_train["knight"].map(
        {
            "Sith": 0,
            "Jedi": 1
        }
    )

    # Create a correlation table dictionary.
    correlation = {
        "features": dataset_train.columns.to_list(),
        "correlation": []
    }

    # Calculate the correlation between each feature and the target.
    for feature in dataset_train.columns:
        correlation["correlation"].append(
            correlation_factor(
                dataset_train[feature],
                dataset_train["knight"]
            )
        )

    # Create a dataframe from the correlation table dictionary.
    correlation = pandas.DataFrame(correlation).sort_values(
        by="correlation", ascending=False
    )

    # Print the correlation table without the index.
    print(correlation.to_string(index=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
