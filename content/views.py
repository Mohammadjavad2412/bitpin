from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from content.models import Post, Score
from content.serializers import PostSerializer, ScoreSerializer
from content.permissions import OnlyAdmin
# Create your views here.


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OnlyAdmin,)


class ScoreView(ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
