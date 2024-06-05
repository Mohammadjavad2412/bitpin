from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from content.models import Post, Score
from content.serializers import PostSerializer, ScoreSerializer
from content.permissions import OnlyAdmin
from django.db.transaction import atomic
from numpy import sqrt
from bitpin.settings import ACCEPTED_NUMBER_OF_SAMPLES
import logging
import traceback


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [OnlyAdmin(),]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        user_id = str(request.user.id)
        user_votes = Score.objects.filter(user_id=user_id).values('post_id', 'rate')
        voted_post_data = {vote['post_id']: vote['rate'] for vote in user_votes}
        result_list = []
        for post_data in response.data:
            result_dict = {}
            result_dict['title'] = post_data['title']
            result_dict['users_votes'] = post_data['rate_count']
            result_dict['average_score'] = post_data['avg_score']
            if post_data['id'] in voted_post_data.keys():
                result_dict['user_rate'] = voted_post_data[post_data['id']]
            result_list.append(result_dict)
        return Response(result_list, status.HTTP_200_OK)


class ScoreView(ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = data['user']
        post_id = data['post']
        is_exists = Score.objects.filter(user_id=user_id, post_id=post_id).exists()
        if is_exists:
            return Response({"error": "user can only vote once for a post"}, status.HTTP_400_BAD_REQUEST)
        post= Post.objects.get(id=post_id)
        old_avg_score = post.avg_score
        if old_avg_score is None:
            post.avg_score = data['rate']
            post.total_score = data['rate']
            post.sum_of_squared_scores = data['rate']**2
            post.rate_count = 1
            post.std_score = 0
            post.save()
        else:
            old_total_score = post.total_score
            old_rate_count = post.rate_count
            old_std_score = post.std_score
            coming_rate = data['rate']
            if old_rate_count > int(ACCEPTED_NUMBER_OF_SAMPLES): #if we reach a certain solid mean score for a post, we can say
                min_valid_vote = old_avg_score - old_std_score #set minimum 
                max_valid_vote = old_avg_score + old_std_score #set maximum
                if int(coming_rate) < min_valid_vote or coming_rate > max_valid_vote: #we can say if we reach a good number of samples, we are not accepting samples higher or lower 1 std from mean 
                    return Response({"error": "dispersion of your vote is very high"}, status.HTTP_400_BAD_REQUEST)
            new_total_score = old_total_score + coming_rate
            new_rate_count = old_rate_count + 1
            new_avg_score = new_total_score / new_rate_count
            old_sum_of_squared_scores = post.sum_of_squared_scores
            squared_score_sample = coming_rate ** 2
            new_sum_of_squared_scores = old_sum_of_squared_scores + squared_score_sample
            std_score = sqrt((new_sum_of_squared_scores / new_rate_count) - (new_avg_score) ** 2)
            post.std_score = std_score
            post.avg_score = new_avg_score
            post.total_score = new_total_score
            post.rate_count = new_rate_count
            post.std_score = std_score
            post.sum_of_squared_scores = new_sum_of_squared_scores
            post.save() 
        return super().create(request, *args, **kwargs)
