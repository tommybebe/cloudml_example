import os
import datetime
import subprocess

import pandas as pd
import xgboost as xgb
from google.cloud import storage
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv

from src.logger import make_logger


load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_ID = os.getenv('BUCKET_ID')


def download(data_dir, local_data_dir):
    print(data_dir)
    bucket = storage.Client(project=PROJECT_ID).bucket('cloud-samples-data')
    blob = bucket.blob(data_dir)
    blob.download_to_filename(local_data_dir)


def get_train_data():
    census_data_filename = 'adult.data.csv'
    data_dir = f'ai-platform/census/data/{census_data_filename}'
    local_data_dir = f'data/{census_data_filename}'

    columns = (
        'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship',
        'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income-level')
    try:
        f = open(local_data_dir)
    except FileNotFoundError as e:
        download(data_dir, local_data_dir)
    finally:
        return pd.read_csv(local_data_dir, header=None, names=columns)


def upload_model(model_name):
    bucket = storage.Client().bucket(BUCKET_ID)
    blob = bucket.blob(f"census/{model_name}")
    blob.upload_from_filename(model_name)


def main():
    log = make_logger('model')
    df = get_train_data()
    target_col = 'income-level'
    categorical_cols = [
        'workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']

    X_train, y_train = df.drop(target_col, axis=1), (df[target_col] == ' >50K')

    encoders = {col: LabelEncoder() for col in categorical_cols}
    for col in categorical_cols:
        X_train[col] = encoders[col].fit_transform(X_train[col])

    log('fitting start')
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)

    log('predict, get accuracy')
    pred = model.predict(X_train)
    score = accuracy_score(pred, y_train)
    log(X_train.head())
    log(score)

    log('upload model')
    model_name = f'model.bst'
    model.save_model(f'trained/{model_name}')
    upload_model(f'trained/{model_name}')
    log('Process finished with exit code 0')


if __name__=='__main__':
    main()
