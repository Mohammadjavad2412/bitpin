from rest_framework import routers
from content.views import PostView, ScoreView
from django.urls import path
from . import views


router = routers.SimpleRouter()
router.register("posts", PostView)
router.register("scores", ScoreView)

app_name = "content"
urlpatterns = [
    
]
urlpatterns += router.urls

