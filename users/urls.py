from rest_framework import routers
from users.views import UserView
from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()
router.register("", UserView)


app_name = "users"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls

