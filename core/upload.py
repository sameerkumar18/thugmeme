import uuid
import os

from imgurpython import ImgurClient

from google.cloud import storage
from google.oauth2 import service_account
from google.cloud.storage import Blob

import boto3


class Upload:

    def __init__(self, provider, credentials, file):
        # if not provider:
        #     raise RuntimeError
        # if not file:
        #     pass
        self.provider = provider
        self.file = file
        self.credentials = credentials

    def upload_file(self):

        if "IMGUR" in self.provider:
            return self.imgur_upload()
        elif "GCP" in self.provider:
            return self.gcp_upload()
        elif "AWS" in self.provider:
            return self.s3_upload()

    '''IMGUR'''

    def imgur_upload(self):
        client_id, client_secret = str(self.credentials).split(',')
        client = ImgurClient(client_id, client_secret)

        return client.upload_from_path(self.file)["link"]

    '''AWS'''

    def s3_upload(self):

        bucket_name, region, access_key, secret_key = self.credentials.split(',')
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        filename = str(uuid.uuid4()) + os.path.splitext(self.file)[-1]
        s3.upload_file(self.file, bucket_name, filename)
        return "https://s3." + region + ".amazonaws.com/" + bucket_name + "/" + filename

    '''GCP'''

    def gcp_upload(self, file_name):
        def authorized_client(cred_file_path, project_name):
            credentials = service_account.Credentials.from_service_account_file(
                cred_file_path)
            client = storage.Client(credentials=credentials, project=project_name)
            return client

        def upload_public_file(client, bkt, file_name):
            # file_name in Blob constructor is the file name you want to have on GCS
            blob = Blob(file_name, bkt)
            # file_name in open function is the one that actually sits on your hard drive
            with open(file_name, 'rb') as my_file:
                blob.upload_from_file(my_file)
            # after uploading the blob, we set it to public, so that it's accessible with a simple link
            blob.make_public(client)
        project_name, bucket_name, cred_file_path = str(self.credentials).split(',')
        client = authorized_client(cred_file_path=cred_file_path, project_name=project_name)
        bkt = client.get_bucket(bucket_name)
        try:
            upload_public_file(client, bkt, file_name=self.file_name)
            return "https://storage.cloud.google.com/" + bucket_name + "/" + self.file_name
        except:
            try:
                self.file_name = "1" + self.file_name
                upload_public_file(client, bkt, file_name=self.file_name)
                return "https://storage.cloud.google.com/" + bucket_name + "/" + file_name
            except:
                raise Exception("Couldn't upload file to GCS")


'''
DUMPED
extension = ""
        if ".png" in filename:
            extension = ".png"
        elif ".jpg" in filename:
            extension = ".jpg"
        elif ".jpeg" in filename:
            extension = ".jpeg"


'''
