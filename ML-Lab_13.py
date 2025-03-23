from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import BaggingClassifier, AdaBoostClassifier, StackingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Load the Iris dataset
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# List of classifiers to evaluate
classifiers = {
    "LogisticRegression": LogisticRegression(max_iter=200),
    "SVC": SVC(probability=True),
    "DecisionTree": DecisionTreeClassifier(),
    "RandomForest": RandomForestClassifier(),
    "GradientBoosting": GradientBoostingClassifier(),
    "GaussianNB": GaussianNB(),
    "KNeighbors": KNeighborsClassifier(),
    "LDA": LinearDiscriminantAnalysis()
}

# Evaluate classifiers
scores = {}
for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    scores[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, average='macro'),
        "Recall": recall_score(y_test, y_pred, average='macro'),
        "F1-Score": f1_score(y_test, y_pred, average='macro')
    }

# Sort classifiers by accuracy and select top 4
sorted_classifiers = sorted(scores.items(), key=lambda x: x[1]["Accuracy"], reverse=True)
top_classifiers = [name for name, _ in sorted_classifiers[:4]]
print("Top 4 classifiers:", top_classifiers)

# Apply ensemble methods
ensemble_results = {}

# Bagging
for clf_name in top_classifiers:
    clf = classifiers[clf_name]
    bagging = BaggingClassifier(estimator=clf, n_estimators=10, random_state=42)
    bagging.fit(X_train, y_train)
    y_pred = bagging.predict(X_test)
    ensemble_results[f"Bagging ({clf_name})"] = accuracy_score(y_test, y_pred)

# Boosting
for clf_name in top_classifiers:
    clf = classifiers[clf_name]
    boosting = AdaBoostClassifier(estimator=clf, n_estimators=10, random_state=42)
    boosting.fit(X_train, y_train)
    y_pred = boosting.predict(X_test)
    ensemble_results[f"Boosting ({clf_name})"] = accuracy_score(y_test, y_pred)

# Stacking
stacking_estimators = [(name, classifiers[name]) for name in top_classifiers]
stacking = StackingClassifier(estimators=stacking_estimators, final_estimator=LogisticRegression())
stacking.fit(X_train, y_train)
y_pred = stacking.predict(X_test)
ensemble_results["Stacking"] = accuracy_score(y_test, y_pred)

# Display results
print("Ensemble Results:")
for method, score in ensemble_results.items():
    print(f"{method}: {score:.4f}")
