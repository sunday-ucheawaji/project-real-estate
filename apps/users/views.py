from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .models import User
from .serializers import UserSerializer


class LoginJWTView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        user = User.objects.get(email=request.data.get("email"))
        if user.is_superuser:
            serializer.validated_data["roles"] = ["admin", "user"]
        else:
            serializer.validated_data["roles"] = ["user"]

        refresh_token = serializer.validated_data.pop("refresh")

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            "refresh_token", refresh_token, max_age=3600, httponly=True, samesite=None
        )

        return response


class LogOutAPIView(generics.RetrieveAPIView):

    def get(self, request: Request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (TokenError, InvalidToken):
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(
            {"data": "No content"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        )
        response.delete_cookie("refresh_token")
        return response


class RefreshJWTView(TokenRefreshView):

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (TokenError, InvalidToken):
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken(refresh_token)
        user = User.objects.get(id=refresh.payload.get("user_id"))
        data = {"access": str(refresh.access_token)}
        if user.is_superuser:
            data["roles"] = ["admin", "user"]
        else:
            data["roles"] = ["user"]

        return Response(data, status=status.HTTP_200_OK)


class UsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=True)
