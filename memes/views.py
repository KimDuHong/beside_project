from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import boto3
from django.conf import settings


class GetUploadURL(APIView):
    @swagger_auto_schema(
        operation_summary="Request for s3 uploadURL",
        operation_description="A POST request to this endpoint returns a pre-signed URL for image upload. It requires a filename to be specified in the request body.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "filename": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The name of the file to be uploaded.",
                )
            },
            required=["filename"],
        ),
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type="object",
                    properties={
                        "url": openapi.Schema(type="string"),
                        "fields": openapi.Schema(
                            type="object",
                            properties={
                                "key": openapi.Schema(type="string"),
                                "AWSAccessKeyId": openapi.Schema(type="string"),
                                "policy": openapi.Schema(type="string"),
                                "signature": openapi.Schema(type="string"),
                            },
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request):
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

        bucket_name = "miimgoo"

        filename = request.data.get("filename")  # Get filename from client
        if not filename:
            return Response({"error": "Filename not provided"}, status=400)

        object_name = f"gif/{filename}.gif"
        response = s3.generate_presigned_post(bucket_name, object_name)
        return Response(response)


class Memes(APIView):
    def get(self, request):
        return Response({1})
