import pandas
import matplotlib.pyplot as plt


def main():

    train = pandas.read_csv("../Train_knight.csv")
    print(train.head())

    train["knight"].replace(["Sith", "Jedi"], [1, 0], inplace=True)
    correlation = train.corr()
    print(correlation)

    # Plot correlation matrix heatmap
    plt.figure(figsize=(12, 10))
    plt.title("Heatmap of Correlation Matrix")
    plt.xlabel("Features")
    plt.ylabel("Features")
    plt.imshow(correlation, cmap="hot")
    plt.colorbar()
    plt.xticks(
        range(len(correlation.columns)), correlation.columns, rotation=90
    )
    plt.yticks(
        range(len(correlation.columns)), correlation.columns
    )
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error in main:", error)
        exit()
