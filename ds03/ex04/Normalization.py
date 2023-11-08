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


def train_mix(axes, dataset_train, mix_features):
    jedi = dataset_train[dataset_train["knight"] == "Jedi"]
    axes[0].scatter(
        jedi[mix_features[0]],
        jedi[mix_features[1]],
        c="red",
        label="Jedi",
        alpha=0.5
    )
    sith = dataset_train[dataset_train["knight"] == "Sith"]
    axes[0].scatter(
        sith[mix_features[0]],
        sith[mix_features[1]],
        c="blue",
        label="Sith",
        alpha=0.5
    )
    axes[0].set_title("Train dataset", fontsize=12)
    axes[0].set_xlabel(mix_features[0], fontsize=10)
    axes[0].set_ylabel(mix_features[1], fontsize=10)
    axes[0].legend(loc="upper right", fontsize=10)
    return axes


def test_mix(axes, dataset_test, mix_features):
    axes[1].scatter(
        dataset_test[mix_features[0]],
        dataset_test[mix_features[1]],
        c="green",
        label="Knight",
        alpha=0.5
    )
    axes[1].set_title("Test dataset", fontsize=12)
    axes[1].set_xlabel(mix_features[0], fontsize=10)
    axes[1].set_ylabel(mix_features[1], fontsize=10)
    axes[1].legend(loc="upper right", fontsize=10)
    return axes


def main():

    # Read the datasets.
    dataset_train = pandas.read_csv("../Train_knight.csv")
    dataset_test = pandas.read_csv("../Test_knight.csv")

    # Standardize the datasets.
    dataset_train_normalized = normalize(dataset_train)
    dataset_test_normalized = normalize(dataset_test)

    print(dataset_train_normalized)
    print(dataset_test_normalized)

    fig, axes = plt.subplots(2, figsize=(10, 9))

    fig.suptitle("Points of the features for the Train and Test datasets")

    mix_features = ["Push", "Deflection"]
    axes = train_mix(axes, dataset_train_normalized, mix_features)
    axes = test_mix(axes, dataset_test_normalized, mix_features)
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
