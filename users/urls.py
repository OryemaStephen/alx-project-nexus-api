from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomLoginView, LoginView

urlpatterns = [
    # JWT auth endpoints
    path("api/token/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Custom login (username/password check)
    path("api/login/", LoginView.as_view(), name="custom_login"),
]
