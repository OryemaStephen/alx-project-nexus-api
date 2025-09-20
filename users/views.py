from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, LoginSerializer


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # Django session login
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                # credentials wrong
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # serializer validation failed (bad request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
