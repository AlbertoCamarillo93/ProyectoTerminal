import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'XXXXX'
SECRET_KEY = 'XXXXX'
SESSION_TOKEN = 'XXXXX'

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Carga exitosa")
        return True
    except FileNotFoundError:
        print("Archivo no encontrado")
        return False
    except NoCredentialsError:
        print("Credenciales no disponibles")
        return False

uploaded = upload_to_aws('carro4.jpg', 'placas-pt1-pruebas-dic2020', 'carro4.jpg')