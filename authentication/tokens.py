from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class CustomAccessToken(AccessToken):
    def add_suap_data(self, id, username, nome_usual, tipo_vinculo, url_foto_75x100, url_foto_150x200):
        #self["type"] = "access"
        #self["suap_token"] = suap_access
        self["id"] = id
        self["username"] = username
        self["nome_usual"] = nome_usual
        self["tipo_vinculo"] = tipo_vinculo
        self["url_foto_75x100"] = url_foto_75x100
        self["url_foto_150x200"] = url_foto_150x200
        
        return self

class CustomRefreshToken(RefreshToken):
    def add_suap_refresh(self, suap_refresh_token):
        self["type"] = "refresh"
        self["suap_refresh_token"] = suap_refresh_token
        return self