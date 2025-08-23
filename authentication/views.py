from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import LoginSerializer
import jwt
from django.conf import settings

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        # Decodificando o access token
        access_token = tokens["access_token"]
        try:
            decoded = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=["HS256"],  # algoritmo padrão do SimpleJWT
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return Response({"error": str(e)}, status=400)

        # Retorna tokens e payload decodificado
        return Response({
            "access": access_token,
            "refresh": tokens["refresh_token"],
            "user_info": tokens["user_info"],
            "decoded_access": decoded
        })


class RefreshView(TokenRefreshView):
    """
    Usa o serializer padrão do SimpleJWT.
    """


class VerifyView(TokenVerifyView):
    """
    Verifica se um token (access ou refresh) é válido.
    """
