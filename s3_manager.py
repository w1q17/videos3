import os
from dotenv import load_dotenv
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# Загружаем переменные окружения из .env файла
load_dotenv()

class MinioManager:
    def __init__(self):
        self.endpoint = os.getenv('MINIO_ENDPOINT')
        self.access_key = os.getenv('MINIO_ACCESS_KEY')
        self.secret_key = os.getenv('MINIO_SECRET_KEY')
        self.s3_client = self._connect_to_minio()

    def _connect_to_minio(self):
        """Создание подключения к MinIO"""
        try:
            s3_config = Config(
                signature_version='s3v4'
            )
            
            s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=s3_config,
                verify=False  # Для самоподписанных сертификатов
            )
            print("Успешное подключение к MinIO")
            return s3_client
        except ClientError as e:
            print(f"Ошибка подключения к MinIO: {e}")
            return None

    def list_buckets(self):
        """Получение списка всех доступных бакетов"""
        try:
            response = self.s3_client.list_buckets()
            print("\nДоступные бакеты:")
            print("-" * 30)
            for bucket in response['Buckets']:
                print(f"Имя бакета: {bucket['Name']}")
                print(f"Дата создания: {bucket['CreationDate']}")
                print("-" * 30)
            return response['Buckets']
        except ClientError as e:
            print(f"Ошибка при получении списка бакетов: {e}")
            return []

def main():
    # Создаем экземпляр менеджера MinIO
    minio_manager = MinioManager()
    
    # Получаем список всех бакетов
    minio_manager.list_buckets()

if __name__ == "__main__":
    main() 