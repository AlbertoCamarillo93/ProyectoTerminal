import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id = 'XXXXX',
    aws_secret_access_key = 'XXXXX',
    aws_session_token = 'XXXXX'
)

s3.download_file('placas-pt1-pruebas-dic2020', 'auto001.jpg', 'client_auto001.jpg')
