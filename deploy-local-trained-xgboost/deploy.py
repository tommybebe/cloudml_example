import os
import datetime
from googleapiclient import errors, discovery
from google.api_core.exceptions import AlreadyExists
from dotenv import load_dotenv

from src.logger import make_logger


load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_ID = os.getenv('BUCKET_ID')

ml = discovery.build('ml','v1')
project_id = f'projects/{PROJECT_ID}'


def new_model(request_dict):
    models = ml.projects().models()
    request = models.create(parent=project_id, body=request_dict)
    model = request.execute()
    return model


def new_version(model, request_dict):
    request = ml.projects().models().versions().create(parent=model['name'], body=request_dict)
    version = request.execute()
    return version


def main():
    log = make_logger('deploy')

    log('get model from cloudml')
    model = new_model({
        'name': 'test_001',
        'description': 'xgboost model with census data'
    })

    log('make new version')
    # check this document for version options
    # https://cloud.google.com/ai-platform/prediction/docs/runtime-version-list
    version = new_version(model, {
        'pythonVersion': '3.7',
        'name': f'ver_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'framework': 'XGBOOST',
        'runtimeVersion': '2.1',
        'deploymentUri': f'gs://{BUCKET_ID}/census/trained'
    })
    print(version)

if __name__=='__main__':
    main()
