from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.openapi import OpenApiParameter, OpenApiTypes

from .models import User
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer, AuthResponseSerializer

@extend_schema(
    operation_id='auth_register',
    summary='Register a new user',
    description='Create a new user account and return JWT tokens',
    request=UserRegistrationSerializer,
    responses={
        201: AuthResponseSerializer,
        400: OpenApiResponse(description='Validation errors')
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    operation_id='auth_login',
    summary='Login user',
    description='Authenticate user and return JWT tokens',
    request=LoginSerializer,
    responses={
        200: AuthResponseSerializer,
        400: OpenApiResponse(description='Invalid credentials')
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    operation_id='get_user_penalties',
    summary='Get user penalty points',
    description='Get penalty points for a specific user. Admins can view any user, users can only view their own penalties.',
    parameters=[
        OpenApiParameter(
            name='id',
            description='User ID',
            required=True,
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: UserSerializer,
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='User not found')
    },
    tags=['User Management']
)
class UserPenaltyView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user_id = self.kwargs['id']
        user = get_object_or_404(User, id=user_id)
        
        # Check permissions - admin can view any user, users can only view themselves
        if not (self.request.user.is_staff or self.request.user.id == user.id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to view this user's penalties.")
        
        return user
