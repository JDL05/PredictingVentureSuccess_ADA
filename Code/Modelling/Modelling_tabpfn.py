import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

from tabpfn import TabPFNClassifier

# load data.csv
data = pd.read_csv('../../Datasets/Saved Sets/data.csv')
# Splitting data into features and target
X = data.drop(columns=['Success'])
y = data['Success']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# Apply SMOTE on the training data, because of the imbalanced target variable (see above)
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

def run_model():
    # Initialize a classifier
    clf = TabPFNClassifier()
    clf.fit(X_train_scaled, y_train_resampled)

    # Predict probabilities
    prediction_probabilities = clf.predict_proba(X_test_scaled)
    print("ROC AUC:", roc_auc_score(y_test, prediction_probabilities[:, 1]))

    # Predict labels
    predictions = clf.predict(X_test_scaled)
    print("Accuracy", accuracy_score(y_test, predictions))

    # Save the model to a file
    with open('tabpfn_model.pkl', 'wb') as model_file:
        pickle.dump(clf, model_file)

    # Save prediction probabilities
    prediction_results = pd.DataFrame({
        'Actual': y_test,
        'Predicted': predictions,
        'Probability': prediction_probabilities[:, 1]
    })
    prediction_results.to_csv('tabpfn_predictions.csv', index=False)

def load():
    # To load the model later:
    with open('tabpfn_model.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)
    # To load the predictions later:
    loaded_predictions = pd.read_csv('tabpfn_predictions.csv')

    predictions = loaded_predictions['Predicted']
    # matrix
    name = "TabPFNClassifier"  # Name of the model
    cm = confusion_matrix(y_test, predictions)
    cm_percentage = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100

    # Display confusion matrix
    cmd = ConfusionMatrixDisplay(cm_percentage, display_labels=["No-Success", "Success"])
    cmd.plot(cmap=plt.cm.Blues, values_format=".2f")
    plt.title(f"Confusion Matrix (Percentage): {name}")
    plt.show()

run_model()