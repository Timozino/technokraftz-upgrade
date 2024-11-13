from .views import MyTokenObtainPairView, RegisterView, PasswordResetVerifyView,PasswordChangeView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/token/", MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", RegisterView.as_view()),
    path("user/passwordReset/<email>/", PasswordResetVerifyView.as_view()),
    path("user/passwordChange/", PasswordChangeView.as_view())
]
