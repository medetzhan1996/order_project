from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import CustomUser
from .permissions import IsOwner
from .serializers import CustomUserCreateSerializer, CustomUserUpdateSerializer, CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    action_serializer_classes = {
        'create': CustomUserCreateSerializer,
        'list': CustomUserSerializer,
        'retrieve': CustomUserSerializer,
        'update': CustomUserUpdateSerializer,
        'partial_update': CustomUserUpdateSerializer,
    }

    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser],
        'retrieve': [IsAuthenticated, IsOwner],
        'update': [IsAuthenticated, IsOwner],
        'partial_update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

    def get_serializer_class(self):
        return self.action_serializer_classes.get(self.action, self.serializer_class)

    def get_permissions(self):
        self.permission_classes = self.permission_classes_by_action.get(
            self.action, [IsAuthenticated, IsOwner])
        return super(CustomUserViewSet, self).get_permissions()


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if phone is None or password is None:
            return Response({'error': 'Both phone and password are required.'}, status=400)

        user = self.authenticate(request, username=phone, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials.'}, status=400)
