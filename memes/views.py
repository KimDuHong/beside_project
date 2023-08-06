from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os
from .models import Meme as Meme_model
from .s3_connect import presigned_s3_upload, presigned_s3_view
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
        filename = f"memes/gif/{filename}"
        response = presigned_s3_upload(filename)
        return Response(response)


class Memes(APIView):
    def get(self, request):
        meme = Meme_model.objects.all()
        serializer = MemeSerializer(meme, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="Create a new meme",
        operation_description="Required URL is s3 endpoint URL",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Title of the meme"
                ),
                "meme_url": openapi.Schema(
                    type=openapi.TYPE_STRING, description="URL of the meme"
                ),
                "tags": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="Tags of the meme, Must be list",
                ),
            },
            required=["title", "meme_url", "tags"],
        ),
        responses={
            201: MemeSerializer(),
            400: "Bad Request ( does not valid data )",
            404: "Not Found ( does not exist tags name )",
        },
    )
    def post(self, request):
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
