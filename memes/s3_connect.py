from django.conf import settings
import boto3
from django.conf import settings


def connect_s3():
    service_name = "s3"
    endpoint_url = "https://kr.object.ncloudstorage.com"
    access_key = settings.NCP_ACCESS_KEY
    secret_key = settings.NCP_SECRET_KEY
    s3 = boto3.client(
        service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    return s3


def presigned_s3_view(filename, ExpiresIn=3600):
    s3 = connect_s3()
    signed_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": "miimgoo", "Key": filename},
        ExpiresIn=ExpiresIn,  # URL이 유효한 시간(초 단위)
    )
    return signed_url


def presigned_s3_upload(filename, ExpiresIn=3600):
    s3 = connect_s3()
    response = s3.generate_presigned_post(
        "miimgoo",
        filename,
        Fields=None,
        Conditions=None,
        ExpiresIn=ExpiresIn,
    )
    return response
