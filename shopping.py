import csv
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

TEST_SIZE = 0.4

def load_data(filename):
    evidence = []
    labels = []

    months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

    #read csv file
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  #Skip the header row
        for row in reader:
            evidence_row = [
                int(row[0]), float(row[1]), int(row[2]), float(row[3]),
                int(row[4]), float(row[5]), float(row[6]), float(row[7]),
                float(row[8]), float(row[9]), months[row[10]],
                int(row[11]), int(row[12]), int(row[13]), int(row[14]),
                1 if row[15] == 'Returning_Visitor' else 0,
                1 if row[16] == 'TRUE' else 0
            ]
            evidence.append(evidence_row)
            labels.append(1 if row[17] == 'TRUE' else 0)
    
    return evidence, labels

def train_model(evidence, labels):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    return sensitivity, specificity

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(evidence, labels, test_size=TEST_SIZE)

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    sensitivity, specificity = evaluate(y_test, predictions)

    correct = (y_test == predictions).sum()
    incorrect = len(y_test) - correct

    print(f"Correct: {correct}")
    print(f"Incorrect: {incorrect}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}")

if __name__ == "__main__":
    main()
