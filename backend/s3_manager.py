import os
from dotenv import load_dotenv
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

load_dotenv()

class MinioManager:
    def __init__(self):
        self.endpoint = os.getenv('MINIO_ENDPOINT')
        self.access_key = os.getenv('MINIO_ACCESS_KEY')
        self.secret_key = os.getenv('MINIO_SECRET_KEY')
        self.s3_client = self._connect_to_minio()

    def _connect_to_minio(self):
        try:
            s3_config = Config(signature_version='s3v4')
            s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=s3_config,
                verify=False
            )
            return s3_client
        except ClientError as e:
            print(f"Ошибка подключения к MinIO: {e}")
            return None

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            print(f"Ошибка создания бакета: {e}")
            return False

    def list_objects(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            objects = []
            for obj in response.get('Contents', []):
                if obj['Key'].lower().endswith(('.mp4', '.avi', '.mov', '.wmv')):
                    objects.append({
                        'name': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
            return objects
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                return None
            print(f"Ошибка получения списка объектов: {e}")
            return []

    def bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False