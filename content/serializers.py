from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from content.models import Post, Score
from numpy import sqrt


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class ScoreSerializer(ModelSerializer):

    class Meta:
        model = Score
        fields = "__all__"

        extra_kwargs = {
            "user": {"required": False},
            "post": {"required": False},
        }

        

    def validate_rate(self, value):
        valid_range = range(0, 6)
        if value in valid_range:
            return value
        else:
            raise serializers.ValidationError("inserted number should be in range of 0 to 5")

    def update(self, instance, validated_data):
        user_new_rate = validated_data.get('rate')
        post_id = instance.post_id
        user_old_rate = instance.rate
        post = Post.objects.get(id=post_id)
        rate_count = post.rate_count
        total_score = post.total_score
        old_sum_of_squared_scores = post.sum_of_squared_scores
        other_users_total_squared_score = old_sum_of_squared_scores - (user_old_rate **2)
        new_total_squared_score = other_users_total_squared_score + (user_new_rate **2)
        other_users_total_score = total_score - user_old_rate
        new_total_score = other_users_total_score + user_new_rate
        avg_score = new_total_score / rate_count
        std_score = sqrt((new_total_squared_score / rate_count) - (avg_score) ** 2)
        post.avg_score = avg_score
        post.total_score = new_total_score
        post.std_score = std_score
        post.sum_of_squared_scores = new_total_squared_score
        post.save()
        return super().update(instance, validated_data)










