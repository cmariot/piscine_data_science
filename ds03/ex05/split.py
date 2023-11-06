import pandas
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_path",
        type=str,
        help="Path to the original dataset",
        default="Train_knight.csv"
    )
    parser.add_argument(
        "--train_path",
        type=str,
        help="Path to the training dataset",
        default="Training_knight.csv"
    )
    parser.add_argument(
        "--validation_path",
        type=str,
        help="Path to the validation dataset",
        default="Validation_knight.csv"
        )
    parser.add_argument(
        "--train_percentage",
        type=float,
        help="Percentage of the train dataset",
        default=0.75
    )
    args = parser.parse_args()
    return (
        args.dataset_path,
        args.train_path,
        args.validation_path,
        args.train_percentage
    )


def fatal_error(error):
    """
    Print the error message and exit the program.
    """
    print(f"\033[91mError: {error}\033[0m")
    exit(1)


def load_dataset(path):
    """
    Load the dataset from a csv file path and return a pandas dataframe.
    """
    dataset = pandas.read_csv(path)
    if dataset.shape[0] < 2:
        fatal_error("The dataset must contains at least two samples.")
    return dataset


def split_dataset(dataset, train_percentage):

    # Check the train_percentage value.
    if train_percentage >= 1 or train_percentage <= 0:
        fatal_error("train_percentage must be between 0 and 1.")

    # Shuffle the dataset.
    dataset = dataset.sample(frac=1)

    # Get the index of the train set.
    dataset_len = len(dataset)
    train_begin_index = 0
    train_end_index = int(dataset_len * train_percentage)
    validation_begin_index = train_end_index
    validation_end_index = dataset_len

    # Check the train and validation sets length.
    if train_end_index == 0 or validation_begin_index == dataset_len:
        fatal_error("train_percentage is too low or too high.")

    # Split the dataset.
    train = dataset[train_begin_index:train_end_index]
    validation = dataset[validation_begin_index:validation_end_index]

    return train, validation


def main(dataset_path, train_path, validation_path, train_percentage):

    # Load the dataset.
    dataset = load_dataset(dataset_path)

    # Split the dataset.
    train, validation = split_dataset(dataset, train_percentage)

    # Save the train and validation sets.
    train.to_csv(train_path, index=False)
    validation.to_csv(validation_path, index=False)


if __name__ == "__main__":

    try:

        (
            dataset_path,
            train_path,
            validation_path,
            train_percentage
        ) = parse_arguments()

        main(
            dataset_path,
            train_path,
            validation_path,
            train_percentage
        )

    except Exception as error:
        print(f"Error: {error}")
        exit(1)
