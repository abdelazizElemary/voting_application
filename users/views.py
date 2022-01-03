from authentication.models import MyToken as AuthToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .models import User
from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer

UserModel = get_user_model()


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        token = AuthToken.objects.create(user=user)

        # send verification otp to email
        email_data = {
            "user_name": user_data["first_name"],
            "otp": user_data["otp"],
        }
        subject = "Email Verification"
        text_content = render_to_string("users/emails/share.txt", email_data)
        html_content = render_to_string("users/emails/share.html", email_data)
        send_mail(
            subject=subject,
            message=text_content,
            from_email="voting-system <noreply@local.vote.com>",
            recipient_list=[request],
            fail_silently=False,
            html_message=html_content,
        )
        res = {
            "user": user_data,
            "token": token.key,
        }
        return Response(res, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_data = UserSerializer(user, context=self.get_serializer_context()).data
        token = AuthToken.objects.create(user=user)
        res = {
            "user": user_data,
            "token": token.key,
        }
        return Response(res, status=status.HTTP_200_OK)


class Logout(generics.GenericAPIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


@api_view(("POST", "GET"))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def verify(request, format=None):
    data = request.data.copy()
    user = User.objects.get(email=data["email"])
    if data["otp"] != user.otp or user.otp_expired:
        raise ValidationError(_("OTP expired"))

    res = {"res": "verified"}
    return Response(res, status=status.HTTP_200_OK)
