from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from memes.models import Meme
from .models import Favoirte_meme


class MemeFavoirtes(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Add/Delete Memes to Favorites",
        operation_description="If the meme exists in Favorites, delete it, if it does not exist, create a new one.",
        responses={
            200: openapi.Response(description="add / deleted"),
            401: openapi.Response(description="The user is not authenticated"),
            404: openapi.Response(description="Not exist Pk"),
        },
    )
    def post(self, request, pk):
        meme = get_object_or_404(Meme, pk=pk)
        like, created = Favoirte_meme.objects.get_or_create(
            user=request.user, meme=meme
        )
        like.delete() if not created else None
        return Response({"add" if created else "deleted"})
