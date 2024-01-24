import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import scipy.stats as stats

from sklearn.pipeline import Pipeline

from feature_engine.imputation import(
    AddMissingIndicator,
    MeanMedianImputer
)

from feature_engine.encoding import CountFrequencyEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler
)

from feature_engine.transformation import (
    YeoJohnsonTransformer,
    LogCpTransformer,
    LogTransformer
)

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
    GridSearchCV,
    RandomizedSearchCV
)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from sklearn.metrics import recall_score, confusion_matrix

import missingno

df = pd.read_csv("e-commerce-dataset.csv")

# see the first 5 of data
df.head()

# row x column
df.shape

# basic information about dataset
df.info()

# drop customer id because it is unnecessary
df = df = df.drop(columns=["CustomerID"], axis=1)

display(df.describe())
display(df.describe(include="O"))

# split categorical and numerical for esier analysis
num_vars = [var for var in df.columns if df[var].dtypes != "O"]
cat_vars = [var for var in df.columns if df[var].dtypes == "O"]

# histogram for each numerical column
df[num_vars].hist(figsize=(10, 10), bins=30)
plt.show()

# check number of unique from numerical variables
df[num_vars].nunique()

# we only normalize variables with more than 10 unique values
num_vars_temp = df[num_vars].nunique()
num_vars_with_more_unique = num_vars_temp[num_vars_temp > 10].index.tolist()

num_vars_with_more_unique

# histogram for more unqie numerical columns
df[num_vars_with_more_unique].hist(figsize=(10, 10), bins=30)
plt.show()

df[num_vars_with_more_unique].describe()

plt.figure(figsize=(12, 5))
for i, var in enumerate(num_vars_with_more_unique):
    plt.subplot(2, 4, i+1)
    stats.probplot(df[var], dist="norm", plot=plt)
    plt.ylabel("RM Quantiles")
    plt.tight_layout()
plt.show()  

# fill missing value with mean
# transformer cannot transform if missing value exist
fill_value = {col:val for (col, val) in zip(num_vars_with_more_unique, df[num_vars_with_more_unique].mean())}
df_temp = df[num_vars_with_more_unique].fillna(value=fill_value)

# define and fit transformer
log_trans = LogCpTransformer(variables=num_vars_with_more_unique)
log_trans.fit(df_temp)

# transform data
df_temp = log_trans.transform(df_temp)

# visualize
plt.figure(figsize=(12, 5))
for i, var in enumerate(num_vars_with_more_unique):
    plt.subplot(2, 4, i+1)
    stats.probplot(df_temp[var], dist="norm", plot=plt)
    plt.ylabel("RM Quantiles")
    plt.tight_layout()
plt.show()  

# fill missing value with mean
# transformer cannot transform if missing value exist
fill_value = {col:val for (col, val) in zip(num_vars_with_more_unique, df[num_vars_with_more_unique].mean())}
df_temp = df[num_vars_with_more_unique].fillna(value=fill_value)

# define and fit transformer
yj_trans = YeoJohnsonTransformer(variables=num_vars_with_more_unique)
yj_trans.fit(df_temp)

# transform data
df_temp = yj_trans.transform(df_temp)

# visualize
plt.figure(figsize=(12, 5))
for i, var in enumerate(num_vars_with_more_unique):
    plt.subplot(2, 4, i+1)
    stats.probplot(df_temp[var], dist="norm", plot=plt)
    plt.ylabel("RM Quantiles")
    plt.tight_layout()
plt.show()  

# check cardinality each columns
df[cat_vars].nunique()

# check rare label each column
for i, var in enumerate(cat_vars):
    ax = plt.subplot(2, 3, i+1)
    df[var].value_counts(normalize=True).plot(kind="bar", ax=ax, figsize=(10, 8))
    plt.axhline(y=0.05, color="red")
    plt.tight_layout()
plt.show()

df.duplicated().sum()

null = df.isna().sum()
null = null[null > 0]/len(df)
null.to_frame(name="% of NaN").join(df[null.index].dtypes.to_frame(name="dtypes"))

df[null.index].describe()

missingno.matrix(df[null.index])
plt.show()

def outlier_check(df, var):

    plt.figure(figsize=(16, 4))

    plt.subplot(1, 3, 1)
    plt.hist(data=df, x=var)
    plt.title(f"Histogram of {var}")

    plt.subplot(1, 3, 2)
    stats.probplot(df[var], dist="norm", plot=plt)
    plt.ylabel("RM Quantiles")
    

    plt.subplot(1, 3, 3)
    sns.boxplot(y = df[var])
    plt.title(f"Boxplot of {var}")

    plt.show()

for var in num_vars_with_more_unique:
    outlier_check(df_temp, var)

# split data to train and test
x_train, x_test, y_train, y_test = train_test_split(
    df.drop(columns=["Churn"], axis=1),
    df["Churn"],
    stratify = df["Churn"],
    test_size = 0.2
)

# configuration
NUMERICAL_VARS_WITH_NA_MEAN = [
    'Tenure'
    , 'WarehouseToHome'
    , 'HourSpendOnApp'
    , 'OrderAmountHikeFromlastYear'
    , 'CouponUsed'
    , 'OrderCount'
    , 'DaySinceLastOrder'
]

CATEGORICAL_ENCODING = [
    'PreferredLoginDevice'
    , 'PreferredPaymentMode'
    , 'Gender'
    , 'PreferedOrderCat'
    , 'MaritalStatus'
]

NUMERICAL_TRANSFORMATION_YEO_JOHNSON = [
    'Tenure'
    , 'WarehouseToHome'
    , 'NumberOfAddress'
    , 'OrderAmountHikeFromlastYear'
    , 'CouponUsed'
    , 'OrderCount'
    , 'DaySinceLastOrder'
    , 'CashbackAmount'
]

NUMERICAL_MINMAX_SCALING = [
    'CityTier'
    , 'HourSpendOnApp'
    , 'NumberOfDeviceRegistered'
    , 'SatisfactionScore'
    , 'Complain'


# define scaler
minmax_scaler = ColumnTransformer([
    ("scaler", MinMaxScaler(feature_range=(0, 1)), NUMERICAL_MINMAX_SCALING)
])

# create data preprocessing pipeline
pipe = Pipeline([
    # add missing indicator
    ("mean_missing_indicator", AddMissingIndicator(variables=NUMERICAL_VARS_WITH_NA_MEAN)),

    # missing value imputation
    ("mean_imputer", MeanMedianImputer(imputation_method="mean", variables=NUMERICAL_VARS_WITH_NA_MEAN)),

    # categorical encoding
    ("freq_encoding", CountFrequencyEncoder(encoding_method="frequency", variables=CATEGORICAL_ENCODING)),

    # yeo johnson transformation
    ("yeo_transform", YeoJohnsonTransformer(variables=NUMERICAL_TRANSFORMATION_YEO_JOHNSON)),
    
    # minmax scaling
    ("scaling", minmax_scaler)    
])

# set output to pandas
pipe.set_output(transform="pandas")

# fitting to data
pipe.fit(x_train, y_train)

# transform
x_train_prep = pipe.transform(x_train)
x_test_prep = pipe.transform(x_test)

# define model
logreg = LogisticRegression(class_weight="balanced")
knn = KNeighborsClassifier()

models = [logreg, knn]

score = []
rata = []
std = []

for mod in models:
    skfold = StratifiedKFold(n_splits=5)
    model_cv = cross_val_score(
        mod,
        x_train_prep,
        y_train,
        cv = skfold,
        scoring="recall"
    )

    score.append(model_cv)
    rata.append(model_cv.mean())
    std.append(model_cv.std())

pd.DataFrame({
    "model" : ["Logistic Regression", "KNN"],
    "recall" : rata,
    "sdev" : std
}).set_index("model").sort_values(by="recall", ascending=False)

# configuration
NUMERICAL_VARS_WITH_NA_MEAN = [
    'Tenure'
    , 'WarehouseToHome'
    , 'HourSpendOnApp'
    , 'OrderAmountHikeFromlastYear'
    , 'CouponUsed'
    , 'OrderCount'
    , 'DaySinceLastOrder'
]

CATEGORICAL_ENCODING = [
    'PreferredLoginDevice'
    , 'PreferredPaymentMode'
    , 'Gender'
    , 'PreferedOrderCat'
    , 'MaritalStatus'
]

# create data preprocessing pipeline
pipe = Pipeline([
    # add missing indicator
    ("mean_missing_indicator", AddMissingIndicator(variables=NUMERICAL_VARS_WITH_NA_MEAN)),

    # missing value imputation
    ("mean_imputer", MeanMedianImputer(imputation_method="mean", variables=NUMERICAL_VARS_WITH_NA_MEAN)),

    # categorical encoding
    ("freq_encoding", CountFrequencyEncoder(encoding_method="frequency", variables=CATEGORICAL_ENCODING)), 
])

# set output to pandas
pipe.set_output(transform="pandas")

# fitting to data
pipe.fit(x_train, y_train)

# transform
x_train_prep = pipe.transform(x_train)
x_test_prep = pipe.transform(x_test)

# define model
dec_tree = DecisionTreeClassifier()
rand_forest = RandomForestClassifier()
xgb = XGBClassifier()

models = [dec_tree, rand_forest, xgb]

score = []
rata = []
std = []

for mod in models:
    skfold = StratifiedKFold(n_splits=5)
    model_cv = cross_val_score(
        mod,
        x_train_prep,
        y_train,
        cv = skfold,
        scoring="recall"
    )

    score.append(model_cv)
    rata.append(model_cv.mean())
    std.append(model_cv.std())

pd.DataFrame({
    "model" : ["Decision Tree", "Random Forest", "XGBoost"],
    "recall" : rata,
    "sdev" : std
}).set_index("model").sort_values(by="recall", ascending=False)

# Define the hyperparameter grid
param_dist = {
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'min_child_weight': [1, 3, 5],
    'subsample': [0.8, 0.9, 1.0],
    'colsample_bytree': [0.8, 0.9, 1.0]
}

# Create an XGBoost classifier
xgb = XGBClassifier()

# Perform RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_dist,
    n_iter=250,  # Number of random combinations to try
    scoring='recall',
    cv=StratifiedKFold(n_splits=5),
    verbose=1,
    n_jobs=-1  # Use all available cores for parallel processing
)

random_search.fit(x_train_prep, y_train)

# Print the best parameters and corresponding accuracy
print("Best Parameters: ", random_search.best_params_)
print("Best recall: ", random_search.best_score_)

# Get the best parameters
best_params = random_search.best_params_

# Create an XGBoost classifier with the best parameters
best_xgb = XGBClassifier(**best_params)

# Fit the model with the best parameters to the entire training set
best_xgb.fit(x_train_prep, y_train)

# predict
y_test_pred = best_xgb.predict(x_test_prep)

print(recall_score(y_test, y_test_pred))

sns.heatmap(confusion_matrix(y_test, y_test_pred), annot=True, fmt="d")
plt.ylabel("y actual")
plt.xlabel("y prediksi")
plt.show()

from xgboost import plot_importance

feature_importance = best_xgb.feature_importances_
plot_importance(best_xgb)
plt.show()