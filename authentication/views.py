from rest_framework.generics import CreateAPIView, get_object_or_404
from authentication import serializers
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.tokens import TokenGenerator
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer, \
    TokenRefreshSerializer
# from notifications.tasks import


class VerifyJSONWebToken(TokenVerifyView):
    """
    post:
    Verify your token (is it valid?)
    To work with API you need to have valid (verified) token which you get after visiting `/auth/token-verify`
    url, entering your token.[Read JWT docs](https://jwt.io/)
    ### Examples
    If data is successfully processed the server returns status code `200`.
    ```json
    {
        "token": "emskdlgnkngdDFHGergergEGRerRGEgerERE346346vergd456456"
    }
    ```
    ### Errors
    If there were some error in client data, it sends status code `401` with the error message looks like:
    ```json
    {
        "detail": "Token is invalid or expired",
        "code": "token_not_valid"
    }
    ```
    """
    serializer_class = TokenVerifySerializer

class SignUpView(CreateAPIView):
    """
    Register new user in the system
    You need to provide `email`, `username`, `password`. All the other information
    is additional
    """
    serializer_class = serializers.SignUpSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        user = serializer.instance
        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{TokenGenerator.make_token(user)}"

        # send_email.delay(
        #     subject="Welcome to Premiers",
        #     template="activation.html",
        #     recipients=[user.email],
        #     context={
        #         'url': utils.construct_url(serializer.validated_data['path'], token),
        #     }
        # )