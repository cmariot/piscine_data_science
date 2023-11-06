import pandas


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


def main():

    # Read the datasets.
    dataset_train = pandas.read_csv("../Train_knight.csv")
    dataset_test = pandas.read_csv("../Test_knight.csv")

    # Standardize the datasets.
    dataset_train_normalized = normalize(dataset_train)
    dataset_test_normalized = normalize(dataset_test)

    print(dataset_train_normalized)
    print(dataset_test_normalized)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)
