import os
import json
from itertools import combinations
from collections import defaultdict
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from urllib.parse import urlparse, urlunparse
from .models import Meme as Meme_model
from .s3_connect import presigned_s3_upload, presigned_s3_view, convert_url_to_presigned
from .serializers import MemeSerializer, MemeDetailSerailizer
from comments.serializers import CommentSerializer


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
            ".GIF",
            ".JPG",
            ".JPEG",
            ".png",
            ".PNG",
        ]:
            return Response({"error": "Filename not provided"}, status=400)
        filename = f"memes/data/{filename}"
        response = presigned_s3_upload(filename)
        return Response(response)


class Memes(APIView):
    @swagger_auto_schema(
        operation_id="Response random 4 memes",
        responses={200: MemeSerializer(many=True)},
    )
    def get(self, request):
        memes = Meme_model.objects.order_by("?")[:4]
        serializer = MemeSerializer(memes, many=True)

        for meme in serializer.data:
            for url_key in ["thumbnail", "meme_url"]:
                convert_url_to_presigned(meme, url_key)

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
    @swagger_auto_schema(
        operation_summary="Response detail meme",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=MemeDetailSerailizer,
            ),
            404: "404 Not Found",
        },
    )
    def get(self, request, pk):
        meme = get_object_or_404(Meme_model, pk=pk)
        meme.visited += 1

        serializer = MemeDetailSerailizer(
            meme,
            context={"request": request},
        )
        data = dict(serializer.data)
        thumbnail_url = data["meme_url"]
        key = urlparse(thumbnail_url).path.lstrip("/").split("miimgoo/")[-1]
        data["meme_url"] = presigned_s3_view(key)
        return Response(data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass


class MemeSearchByTag(APIView):
    @swagger_auto_schema(
        operation_summary="Search by tag",
        operation_description="Request with the tag of the meme to be searched as a parameter",
        manual_parameters=[
            openapi.Parameter(
                "tags",
                in_=openapi.IN_QUERY,
                description="Tags for the search",
                required=True,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                collection_format="multi",
            )
        ],
        responses={200: "Success", 400: "Bad Request"},
    )
    def get(self, request):
        tag_json = request.GET.get("tags", "[]")

        try:
            tag_list = json.loads(tag_json)
        except json.JSONDecodeError:
            return Response({"error": "Invalid tag format"})

        if not isinstance(tag_list, list):
            return Response({"error": "NOT LIST"})

        if not tag_list:
            raise ParseError

        results_by_combinations = {}

        all_tagged_memes = Meme_model.objects.filter(
            tags__name__in=tag_list
        ).values_list("id", "tags__name")

        filtered_memes_by_tag = defaultdict(set)
        for meme_id, tag_name in all_tagged_memes:
            filtered_memes_by_tag[tag_name].add(meme_id)

            # Prefetch related tags for better performance
        all_memes_with_tags = Meme_model.objects.prefetch_related("tags")

        # Iterate through tag combinations starting with the longest combination
        for r in range(len(tag_list), 0, -1):
            for tag_combination in combinations(tag_list, r):
                combined_meme_ids = filtered_memes_by_tag[tag_combination[0]].copy()
                for tag in tag_combination[1:]:
                    combined_meme_ids &= filtered_memes_by_tag[tag]

                # Fetch the actual meme objects from the IDs
                combined_memes = [
                    meme for meme in all_memes_with_tags if meme.id in combined_meme_ids
                ]

                serializer = MemeSerializer(combined_memes, many=True)
                for meme in serializer.data:
                    for field in ["thumbnail", "meme_url"]:
                        url = meme[field]
                        key = urlparse(url).path.lstrip("/").split("miimgoo/")[-1]
                        meme[field] = presigned_s3_view(key)

                results_by_combinations[", ".join(tag_combination)] = serializer.data

                # Exclude the memes we've already processed
                for tag in tag_list:
                    filtered_memes_by_tag[tag] -= combined_meme_ids

        results_by_combinations = {
            k: v for k, v in results_by_combinations.items() if v
        }

        return Response(results_by_combinations)


class DetailMemeComment(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Create comment about meme",
        operation_description="memes id required",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["description"],
            properties={
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Comment content"
                )
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful Response", schema=CommentSerializer
            ),
            400: "Description 형식 오류",
            403: "Login Error",
            404: "존재하지 않는 feed pk",
        },
    )
    def post(self, request, pk):
        meme = get_object_or_404(Meme_model, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(meme=meme, user=request.user)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
