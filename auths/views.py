from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from utils.jwt import decode_token, generate_access_token, generate_refresh_token
from home.models import User, RefreshToken
from home.serializers import UserSerializers
from auths.serializers import AuthSerializer, UserDataSerializer, RegisterSerializer, UpdateUserSerializer, ChangePasswordSerializer, RefreshTokenSerializer
from middlewares import auth_middleware
from utils.redis import set_cache
from utils.response import success_response, failure_response
import jwt
from PythonWeb.settings import JWT_SECRET
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


@swagger_auto_schema(
    method='POST',
    operation_description="Login by Email",
    tags=["Auth"],
    request_body=AuthSerializer,
    responses={
        200: openapi.Response(
            "Success", examples={"application/json": {"message": "Success"}}
        ),
        400: openapi.Response(
            "Validation Error", examples={"application/json": {"error": "Invalid input"}}
        )
    },
    security=[]
)
@api_view(['POST'])
def login(request, *args, **kwargs):

    serializer = AuthSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    try:
        user = User.objects.get(email=email)
        if user.check_password(password) == False:
            return failure_response(data={"message": "Password is incorrect"}, status_code=status.HTTP_404_NOT_FOUND)

        user_data = UserSerializers(user).data

        access_token = generate_access_token(
            user_data['id'], user_data['is_staff'])
        refresh_token = generate_refresh_token(user_data['id'])

        expires_at = datetime.now(timezone.utc) + timedelta(days=30)

        is_existed_fresh_token = RefreshToken.objects.filter(user=user).first()

        if not is_existed_fresh_token:
            new_refresh_token = RefreshToken.objects.create(
                user=user, expires_at=expires_at, token=refresh_token)
            new_refresh_token.save()
        else:
            is_existed_fresh_token.token = refresh_token
            is_existed_fresh_token.expires_at = expires_at
            is_existed_fresh_token.save()

        profile = UserDataSerializer(user).data
        set_cache(f'access_token:{access_token}', access_token, 6000)
        return success_response(data={'access_token': access_token, 'refresh_token': refresh_token, 'data': profile}, status_code=200)
    except User.DoesNotExist:
        return success_response(data={"message": "Not found user"}, status_code=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='POST',
    operation_description="Register account",
    tags=["Auth"],
    request_body=RegisterSerializer,
    responses={},
    security=[]
)
@api_view(['POST'])
def register(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = User.objects.filter(email=email).first()
    if user:
        return failure_response(message='Email is already taken', status_code=status.HTTP_409_CONFLICT)

    new_user = User(
        email=email,
        is_staff=False
    )
    new_user.set_password(password)
    new_user.save()

    user_data = UserSerializers(new_user).data
    return success_response(data=user_data)

@swagger_auto_schema(
    method='PATCH',
    operation_description="Update profile",
    tags=["Auth"],
    request_body=UpdateUserSerializer,
    responses={},
    security=[{"Bearer": []}],
)
@swagger_auto_schema(
    method='GET',
    operation_description="Get profile",
    tags=["Auth"],
    responses={},
    security=[{"Bearer": []}],
)
@api_view(['GET', 'PATCH'])
@auth_middleware
def profile_view(request, *args, **kwargs):
    user_id = request.user['id']

    if request.method == 'GET':
        user = get_object_or_404(User, id=user_id)
        user_data = UserDataSerializer(user).data
        return Response(data=user_data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        serializer = UpdateUserSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        user_name = serializer.validated_data.get('user_name')

        user = get_object_or_404(User, id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = user_name
        user.save()

        return Response(status=status.HTTP_200_OK, data=UserDataSerializer(user).data)

@swagger_auto_schema(
    method='PATCH',
    operation_description="Change password",
    tags=["Auth"],
    request_body=ChangePasswordSerializer,
    responses={},
    security=[{"Bearer": []}],
)
@api_view(['PATCH'])
@auth_middleware
def change_password(request, *args, **kwargs):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)

    user_id = request.user['id']
    current_password = serializer.validated_data['current_password']
    new_password = serializer.validated_data['new_password']
    refresh_token = serializer.validated_data['refresh_token']

    try:
        decoded = decode_token(refresh_token)
    except jwt.ExpiredSignatureError:
        return failure_response(message="Refresh Token expired", status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return failure_response(message="Invalid Refresh Token", status_code=status.HTTP_401_UNAUTHORIZED)

    user = get_object_or_404(User, id=user_id)

    if not user.check_password(current_password):
        return failure_response(message='Current password is incorrect', status_code=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    old_refresh_token = get_object_or_404(RefreshToken, user_id=user_id)
    old_refresh_token.token = generate_refresh_token(user_id)
    old_refresh_token.save()

    user_data = UserDataSerializer(user).data
    return success_response(status=status.HTTP_200_OK, data=user_data)

@swagger_auto_schema(
    method='POST',
    operation_description="Refresh access token",
    request_body=RefreshTokenSerializer,
    tags=["Auth"],
    responses={},
    security=[{"Bearer": []}],
)
@api_view(['POST'])
def refresh_token(request, *args, **kwargs):
    serializer = RefreshTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return failure_response(data=serializer.errors)

    refresh_token = serializer.validated_data['refresh_token']

    old_refresh_token = RefreshToken.objects.filter(token=refresh_token).first()
    if not old_refresh_token:
        return failure_response(status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid refresh token")

    try:
        decoded = decode_token(refresh_token)
        user = get_object_or_404(User, id=decoded['id'])
        new_access_token = generate_access_token(id=decoded['id'], role=user.is_staff)
        
        set_cache(f'access_token:{new_access_token}', new_access_token, 6000)

        return success_response(status_code=200, data={"new_access_token": new_access_token})

    except jwt.ExpiredSignatureError:
        return failure_response(message="Refresh Token expired", status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return failure_response(message="Invalid Refresh Token", status_code=status.HTTP_401_UNAUTHORIZED)