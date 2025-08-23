from rest_framework import serializers
from django.contrib.auth import authenticate
from .tokens import CustomAccessToken, CustomRefreshToken
import requests

SUAP_API_LOGIN = "https://suap.ifsuldeminas.edu.br/api/token/pair"
SUAP_API_ME = "https://suap.ifsuldeminas.edu.br/api/v2/minhas-informacoes/meus-dados/"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        data={"username": username, "password": password}

        # 1️⃣ Solicita token ao SUAP
        r = requests.post(SUAP_API_LOGIN, json=data)
        if r.status_code != 200:
            raise serializers.ValidationError("Credenciais inválidas SUAP")
        suap_tokens = r.json()
        suap_access = suap_tokens.get("access")
        suap_refresh = suap_tokens.get("refresh")

        # 2️⃣ Busca dados do usuário no SUAP (nome, foto, etc)
        headers = {"Authorization": f"Bearer {suap_access}"}
        r_info = requests.get(SUAP_API_ME, headers=headers)
        if r_info.status_code != 200:
            raise serializers.ValidationError("Não foi possível obter informações do usuário")
        suap_info = r_info.json()
        id = suap_info.get("id", None)
        nome_usual = suap_info.get("nome_usual", None)
        tipo_vinculo = suap_info.get("tipo_vinculo", None)
        url_foto_75x100 = suap_info.get("url_foto_75x100", None)
        url_foto_150x200 = suap_info.get("url_foto_150x200", None)
        
        # 3️⃣ Cria access_token manualmente
        access = CustomAccessToken()
        access["id"] = id
        access["username"] = username
        access["nome_usual"] = nome_usual
        access["tipo_vinculo"] = tipo_vinculo
        access["url_foto_75x100"] = url_foto_75x100
        access["url_foto_150x200"] = url_foto_150x200
        

        # 4️⃣ Cria refresh_token manualmente
        refresh = CustomRefreshToken()
        refresh["type"] = "refresh"
        refresh["suap_refresh_token"] = suap_refresh

        return {
            "access_token": str(access),
            "refresh_token": str(refresh),
            "user_info": {
                "id": id,
                "username": username,
                "nome_usual": nome_usual,
                "tipo_vinculo": tipo_vinculo,
                "url_foto_75x100": url_foto_75x100,
                "url_foto_150x200": url_foto_150x200
            }
        }