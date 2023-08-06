from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from urllib.parse import urlparse, urlunparse
import os

from .s3_connect import connect_s3, presigned_s3_upload, presigned_s3_view
from .serializers import MemeSerializer


class GetUploadURL(APIView):
    @swagger_auto_schema(
        operation_summary="Request for s3 uploadURL",
        operation_description="A POST request to this endpoint returns a pre-signed URL for image upload. It requires a filename to be specified in the request body.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "filename": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The name of the file to be uploaded. Contains .gif",
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
            400: openapi.Response(
                description="Error, if filename null or does not contain .gif or .jpg or .jpeg"
            ),
        },
    )
    def post(self, request):
        filename = request.data.get("filename")  # Get filename from client

        if not filename or os.path.splitext(filename)[1] not in [
            ".gif",
            ".jpg",
            ".jpeg",
        ]:
            return Response({"error": "Filename not provided"}, status=400)
        filename = f"gif/{filename}"
        response = presigned_s3_upload(filename)
        return Response(response)


class Memes(APIView):
    def get(self, request):
        pass

    def post(self, request):
        url = request.data.get("meme_url")
        parsed_url = urlparse(url)
        cleaned_url = urlunparse(parsed_url._replace(query=""))
        request.data["meme_url"] = cleaned_url

        serializer = MemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tags=request.data.get("tags"))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DetailMeme(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
