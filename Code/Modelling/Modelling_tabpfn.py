import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tabpfn import TabPFNClassifier

# load data.csv
data = pd.read_csv('../../Datasets/Aggregated Sets/data.csv')
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

# Initialize a classifier
clf = TabPFNClassifier()
clf.fit(X_train_scaled, y_train_resampled)

# Predict probabilities
prediction_probabilities = clf.predict_proba(X_test_scaled)
print("ROC AUC:", roc_auc_score(y_test, prediction_probabilities[:, 1]))

# Predict labels
predictions = clf.predict(X_test_scaled)
print("Accuracy", accuracy_score(y_test, predictions))