import pandas
import matplotlib.pyplot as plt


def normalize(dataset):
    """
    Normalize the dataset.
    """
    for feature in dataset.columns:
        if dataset[feature].dtype != "object":
            dataset[feature] = (
                dataset[feature] - dataset[feature].min()
            ) / (dataset[feature].max() - dataset[feature].min())
    return dataset


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

    train = pandas.read_csv("../Train_knight.csv")
    print(train.head())
    # train["knight"].replace(["Sith", "Jedi"], [1, 0], inplace=True)
    # train.drop("knight", axis=1, inplace=True)

    train = normalize(train)

    # Calculate the variance of each feature as a percentage
    variance = train.var(
        numeric_only=True
    )

    explain_variance = variance / variance.sum() * 100
    explain_variance = explain_variance.sort_values(ascending=False)

    cumulative_variance = explain_variance.cumsum()

    # Plot cumulative variance
    plt.plot(
        range(len(cumulative_variance)),
        cumulative_variance
    )
    plt.xlabel("Number of features")
    plt.ylabel("Cumulative variance")
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error in main:", error)
        exit()
