import pandas as pd
import numpy as np

# Load fake data and assign it label 0
fake = pd.read_csv("news/fake.csv")
fake["label"] = 0

# Load true data and assign it label 1
true = pd.read_csv("news/true.csv")
true["label"] = 1

# Combine the 2 datasets, and shuffle them to avoid model bias from order
df = pd.concat([true, fake], ignore_index=True)
df = df.sample(frac=1, random_state=2025).reset_index(drop=True)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

# Preprocessing function: converts text to lowercase and removes punctuation
from preprocessing import clean

# Split data into training and testing sets
# Stratify to maintain label distribution in both sets

# NOTE: only the Title data is being looked at here
X_train, X_test, y_train, y_test = train_test_split(
    df.title,
    df.label,
    test_size=0.2,
    random_state=2025,
    stratify=df.label
)

# NOTE: only the Text data is being looked at here
X2_train, X2_test, y2_train, y2_test = train_test_split(
    df.text,
    df.label,
    test_size=0.2,
    random_state=2025,
    stratify=df.label
)

# Machine Learning Pipeline with TDIDF Vectorizer and Logistic Regression
clf = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', preprocessor=clean)),
    ('log', LogisticRegression(solver='lbfgs', max_iter=1000))
])

# Hyperparameter grid
param_grid = {
    'tfidf__max_df': [0.7, 0.85, 1.0],
    'tfidf__min_df': [1, 3, 5],
    'tfidf__ngram_range': [(1,1), (1,2)],
    'log__C': [0.1, 1, 10]
}

# Set up grid search with 5-fold cross-validation,
# scoring by F1 score to balance precision and recall,
# verbose output and parallel computation enabled
grid = GridSearchCV(
    clf,
    param_grid,
    cv=5,
    scoring='f1',
    verbose=1,
    n_jobs=-1
)

# Train model and search for best hyperparameters on TITLE training data
grid.fit(X_train, y_train)
best_model_title = grid.best_estimator_

# Report on Title
# y_pred = best_model_title.predict(X_test)
# print(classification_report(y_test, y_pred))    

# Cloning best Title model and tuning it for Text
# Did not run a full Grid Search on the hyperparameters since there is too much text data,
# and I do not have the computing power
from sklearn.base import clone

text_model = clone(best_model_title)

text_model.set_params(
    tfidf__ngram_range=(1, 2),
    tfidf__max_df=0.85 
)

text_model.fit(X2_train, y2_train)

import joblib

# Serializing Models
joblib.dump(best_model_title, "title_model.job")
joblib.dump(text_model, "text_model.job")