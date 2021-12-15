import boto3
from botocore.exceptions import NoCredentialsError
import config

config.ACCESS_KEY = 'XXXXX'
config.SECRET_KEY = 'XXXXX'
config.SESSION_TOKEN = 'XXXXX'

def upload_to_aws():

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id='AKIAZ56RHXMENRCBKN5H',
        aws_secret_access_key='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'
    )

    path = f"D:\Aplicaciones\Yolo_v4\yolov4-custom-functions\detections\\archivosTxtOCR\\ocrDetect1.png"

    s3.Bucket('reporte-alerta-guardado').upload_file(Filename=path, Key='ocrDetect1_AWS.png')


uploaded = upload_to_aws()