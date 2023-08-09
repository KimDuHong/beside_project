from rest_framework.views import APIView
from .models import Tag
from .serializers import TagSerializer, GroupTagSerializer
from rest_framework.response import Response


class AllTagView(APIView):
    type_mapping = {"circum": "상황", "emotion": "감정", "people": "인물", "other": "기타"}

    def get(self, request):
        tag_type = request.GET.get("type")  # type 파라미터를 가져옵니다.
        tag_type_kor = self.type_mapping.get(tag_type)

        if tag_type_kor:
            tags = Tag.objects.filter(type=tag_type_kor)  # 해당 type에 맞는 태그만 필터링하여 가져옵니다.
        else:
            tags = Tag.objects.all()

        serializer = TagSerializer(tags, many=True)

        if tag_type_kor:
            return Response({tag_type_kor: [item["name"] for item in serializer.data]})

        # 모든 태그 데이터를 초기화합니다.
        result = {
            "상황": [item["name"] for item in serializer.data if item["type"] == "상황"],
            "감정": [item["name"] for item in serializer.data if item["type"] == "감정"],
            "인물": [item["name"] for item in serializer.data if item["type"] == "인물"],
            "기타": [item["name"] for item in serializer.data if item["type"] == "기타"],
        }

        return Response(result)

    def post(self, request):
        serializer = TagSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TagDetailVeiw(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
