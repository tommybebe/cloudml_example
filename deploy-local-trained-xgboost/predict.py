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


def get_model(name):
    models = ml.projects().models()
    model = models.get(name=name).execute()
    return model


def predict(project, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    service = discovery.build('ml', 'v1')
    name = model

    if version is not None:
        name += f'/versions/{version}'

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']


def main():
    instances = [
        [50,4,153931,11,9,0,1,1,4,0,0,0,40,39],
        [31,4,182896,11,9,4,3,1,4,0,0,0,40,39],
        [63,0,221592,11,9,2,0,0,4,1,0,0,40,39],
        [48,4,155664,11,9,2,3,0,4,1,7688,0,70,39],
        [29,4,114801,15,10,2,4,0,4,1,0,0,40,39],
    ]
    model = get_model('projects/vibrant-airship-281001/models/test_001')
    pred = predict(PROJECT_ID, model['name'], instances)
    print(pred)
    # [0.05539296567440033, 0.024639282375574112, 0.26205211877822876, 0.982042133808136, 0.3104497790336609]


if __name__=='__main__':
    main()
