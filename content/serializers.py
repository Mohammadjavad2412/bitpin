from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from content.models import Post, Score


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class ScoreSerializer(ModelSerializer):

    voted_users_num = serializers.SerializerMethodField()
    avg_vote = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = "__all__"

    
    def get_voted_users_num(self, obj):
        pass
        

    def get_avg_vote(self, obj):
        pass

    def get_user_vote(self, obj):
        pass





