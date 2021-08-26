from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication import serializers
from authentication.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.tokens import TokenGenerator
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer, \
    TokenRefreshSerializer
from rest_framework.response import Response
from authentication import utils
from authentication.schema import JSONTokenSchema
from notifications.tasks import send_email


class VerifyJSONWebToken(TokenVerifyView):
    serializer_class = TokenVerifySerializer

class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        user = serializer.instance
        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{TokenGenerator.make_token(user)}"

        send_email.delay(
            subject="Welcome to Reminder",
            template="activation.html",
            recipients=[user.email],
            # context={
            #     'url': utils.construct_url(serializer.validated_data['path'], token),
            # }
         )

class ActivateUserView(APIView):
    serializer_class = serializers.ActivationTokenSerializer

    @swagger_auto_schema(
        request_body=serializers.ActivationTokenSerializer,
        response={
            '200': JSONTokenSchema
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate_user()
        user = get_object_or_404(User, email=serializer.validated_data['email'])
        token = RefreshToken.for_user(user)
        return Response(data={'access': str(token.access_token),
                              'refresh': str(token)})