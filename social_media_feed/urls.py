from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import LoginView, CustomLoginView
from django.http import JsonResponse
from graphene_file_upload.django import FileUploadGraphQLView

def health_check(request):
    return JsonResponse({"status": "ok"})


def home(request):
    return JsonResponse({"message": "Welcome to Nexus API"})


urlpatterns = [
    path("healthz", health_check),  # health check endpoint
    path("", home, name="home"),    # root endpoint
    path("admin/", admin.site.urls),
    
    #  # --- GraphQL (with file upload support) ---
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
    
    # --- Auth routes (REST/JWT) ---
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/token/", CustomLoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # --- App routes ---
    path("api/users/", include("users.urls")), 
    
]
