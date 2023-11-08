import numpy as np
import matplotlib.pyplot as plt
import pandas


def plot_cm(cm, classes, title, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, ha="right")
    plt.yticks(tick_marks, classes)
    # Put the values inside the confusion matrix
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = cm.iloc[i, j]
            plt.text(
                j,
                i,
                format(value, "d"),
                ha="center",
                va="center",
                color="white" if value > 26 else "black"
            )
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.show()


def confusion_matrix_(y_true, y_hat, labels, df_option=False):
    """
        Compute confusion matrix to evaluate the accuracy of a classification.
        Args:
            y: a numpy.array for the correct labels
            y_hat: a numpy.array for the predicted labels
            labels: optional, a list of labels to index the matrix.
                    This may be used to reorder or select a subset of labels.
            df_option: optional, if set to True the function will return a
                       pandas DataFrame instead of a numpy array.
                       (default=False)
        Return:
            The confusion matrix as a numpy array or a pandas DataFrame
            according to df_option value.
            None if any error.
        Raises:
            This function should not raise any Exception.
    """

    try:
        if y_true.shape != y_hat.shape:
            raise ValueError("y_true and y_hat must have the same shape")
        if y_true.size == 0 or y_hat.size == 0:
            raise ValueError("y_true and y_hat must not be empty")

        cm = np.zeros((len(labels), len(labels)), dtype=int)
        for i in range(len(labels)):
            for j in range(len(labels)):
                cm[i, j] = np.sum((y_true == labels[i]) & (y_hat == labels[j]))

        if df_option:
            cm = pandas.DataFrame(cm, index=labels, columns=labels)

        print(cm, "\n")
        return cm

    except Exception as error:
        print("Error in confusion_matrix_:", error)
        exit()


def accuracy_score_(y, y_hat):
    """
    Compute the accuracy score.
    Accuracy tells you the percentage of predictions that are accurate
    (i.e. the correct class was predicted).
    Accuracy doesn't give information about either error type.
    Args:
        y: a numpy.ndarray for the correct labels
        y_hat:a numpy.ndarray for the predicted labels
    Returns:
        The accuracy score as a float.
        None on any error.
    Raises:
        This function should not raise any Exception.
    """

    try:
        if not isinstance(y, np.ndarray) \
                or not isinstance(y_hat, np.ndarray):
            raise TypeError("y and y_hat must be numpy.ndarrays")
        elif y.shape != y_hat.shape:
            raise ValueError("y and y_hat must have the same shape")
        elif y.size == 0:
            raise ValueError("y and y_hat must not be empty")
        accuracy = np.mean(y == y_hat)
        return accuracy

    except Exception as error:
        print(error)
        exit()


def f1_score_(y, y_hat, pos_label=1):
    """
    Compute the f1 score.
    F1 score combines precision and recall in one single measure.
    You use the F1 score when want to control both
    False positives and False negatives.
    Args:
        y: a numpy.ndarray for the correct labels
        y_hat: a numpy.ndarray for the predicted labels
        pos_label: str or int, the class on which to report
                the precision_score (default=1)
    Returns:
        The f1 score as a float.
        None on any error.
    Raises:
        This function should not raise any Exception.
    """
    try:
        if not isinstance(y, np.ndarray) \
                or not isinstance(y_hat, np.ndarray):
            return None

        if y.shape != y_hat.shape:
            return None

        if y.size == 0 or y_hat.size == 0:
            return None

        if not isinstance(pos_label, (int, str)):
            return None

        precision = precision_score_(y, y_hat, pos_label)
        recall = recall_score_(y, y_hat, pos_label)

        if precision is None or recall is None:
            return 0.0
        if precision + recall == 0:
            return 0.0

        return 2 * (precision * recall) / (precision + recall)

    except Exception:
        return 0.0


def precision_score_(y, y_hat, pos_label=1):
    """
    Compute the precision score.
    Precision tells you how much you can trust your
    model when it says that an object belongs to Class A.
    More precisely, it is the percentage of the objects
    assigned to Class A that really were A objects.
    You use precision when you want to control for False positives.
    Args:
        y: a numpy.ndarray for the correct labels
        y_hat: a numpy.ndarray for the predicted labels
        pos_label: str or int, the class on which to report
                the precision_score (default=1)
    Return:
        The precision score as a float.
        None on any error.
    Raises:
        This function should not raise any Exception.
    """
    try:
        if not isinstance(y, np.ndarray) \
                or not isinstance(y_hat, np.ndarray):
            return None

        if y.shape != y_hat.shape:
            return None

        if y.size == 0 or y_hat.size == 0:
            return None

        if not isinstance(pos_label, (int, str)):
            return None

        tp = np.sum(np.logical_and(y == pos_label, y == y_hat))
        fp = np.sum(np.logical_and(y != pos_label, y_hat == pos_label))

        if tp + fp == 0:
            return 0.0

        return tp / (tp + fp)

    except Exception:
        return 0


def recall_score_(y, y_hat, pos_label=1):
    """
    Compute the recall score.
    Recall tells you how much you can trust that your
    model is able to recognize ALL Class A objects.
    It is the percentage of all A objects that were properly
    classified by the model as Class A.
    You use recall when you want to control for False negatives.
    Args:
        y:a numpy.ndarray for the correct labels
        y_hat:a numpy.ndarray for the predicted labels
        pos_label: str or int, the class on which to report
                the precision_score (default=1)
    Return:
        The recall score as a float.
        None on any error.
    Raises:
        This function should not raise any Exception.
    """
    try:
        if not isinstance(y, np.ndarray) \
                or not isinstance(y_hat, np.ndarray):
            return None

        if y.shape != y_hat.shape:
            return None

        if y.size == 0 or y_hat.size == 0:
            return None

        if not isinstance(pos_label, (int, str)):
            return None

        tp = np.sum(np.logical_and(y == pos_label, y == y_hat))
        fn = np.sum(np.logical_and(y == pos_label, y_hat != pos_label))

        if tp + fn == 0:
            return 0.0

        return tp / (tp + fn)

    except Exception:
        return None


def read_file(path: str) -> np.ndarray:
    with open(path, "r") as file:
        data = file.readlines()
        return np.array([line.strip() for line in data])


if __name__ == "__main__":

    try:

        truth = read_file("../truth.txt")
        prediction = read_file("../predictions.txt")

        cm = confusion_matrix_(
            truth,
            prediction,
            labels=["Jedi", "Sith"],
            df_option=True
        )

        metrics_df = pandas.DataFrame(
            {
                "Precision": [
                    precision_score_(truth, prediction, "Jedi"),
                    precision_score_(truth, prediction, "Sith"),
                ],
                "Recall": [
                    recall_score_(truth, prediction, "Jedi"),
                    recall_score_(truth, prediction, "Sith")
                ],
                "F1-Score": [
                    f1_score_(truth, prediction, "Jedi"),
                    f1_score_(truth, prediction, "Sith")
                ],
                "Size": [
                    np.sum(truth == "Jedi"),
                    np.sum(truth == "Sith")
                ]
            },
            index=["Jedi", "Sith"]
        )
        last_line = pandas.DataFrame(
            {
                "Accuracy": [
                    accuracy_score_(truth, prediction)
                ],
                "Size": [
                    len(truth)
                ]
            },
            index=["Total"]
        )

        print(metrics_df, "\n\n", last_line)

        plot_cm(cm, ["Jedi", "Sith"], "Confusion Matrix")

    except Exception as error:
        print("Error in main:", error)
        exit()
