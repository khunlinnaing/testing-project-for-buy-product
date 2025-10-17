from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model

from project.serializers.attentedSerializer import WorkLogSerializer
from project.serializers.saleSerializer import SaleSerializer
from .serializers.loginSerializer import LoginSerializer
from .serializers.registerSerializer import RegisterSerializer  # new serializer
from .serializers.purchaseSerializer import PurchaseSerializer
from django.utils import timezone
from django.contrib.auth import login
from rest_framework.views import APIView
from .serializers.userSerializer import UserSerializer
from .models import *

from django.db.models.functions import TruncDate
from django.db.models import F, Sum
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()

token_param = openapi.Parameter(
    name="Authorization",
    in_=openapi.IN_HEADER,
    description="Token <your_token>",
    type=openapi.TYPE_STRING,
    required=True,
)

def item_swagger(operation_description="", tagname="", requestdata=None, method="GET"):
    if method.upper() in ["POST", "PUT", "DELETE"]:
        return swagger_auto_schema(
            operation_description=operation_description,
            tags=[tagname],
            manual_parameters=[token_param],
            request_body=requestdata,
        )
    return swagger_auto_schema(
        operation_description=operation_description,
        tags=[tagname],
        manual_parameters=[token_param],
    )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User login",
        tags=["Auth"],
        request_body=LoginSerializer,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data

            return Response({
                'success': True,
                'token': token.key,
                'userid': user.id,
                'user': user_data
            }, status=status.HTTP_200_OK)

        return Response({
            "error": "Invalid credentials. Please try again.",
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_description="User registration",
        tags=["Auth"],
        request_body=RegisterSerializer,
    )
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




token_param2 = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description='Token <your_token>',
    type=openapi.TYPE_STRING,
    required=True
)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete'] 
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.filter(is_staff=True).order_by('-id')

    @item_swagger("Get all user", "User", method="GET")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @item_swagger("Get a single user", "User", method="GET")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @item_swagger("update user", "User", requestdata=UserSerializer, method='PUT')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @item_swagger("delete user", "User", method='DELETE')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        profile_data = serializer.validated_data.get('profile', None)
        if profile_data:
            profile_data['user'] = self.request.user
        serializer.save()
    
class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'purchase_no']

    def get_queryset(self):
        """
        Superusers: See all purchases created today.
        Normal users: See only their own purchases created today.
        """
        today = timezone.localdate()
        if self.request.user.is_superuser:
            return Purchase.objects.filter(create_date__date=today).order_by('-id')
        return Purchase.objects.filter(user=self.request.user, create_date__date=today).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and serializer.instance.user != self.request.user:
            raise PermissionDenied("You cannot update another user's purchase")
        serializer.save(user=serializer.instance.user)

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.user != self.request.user:
            raise PermissionDenied("You cannot delete another user's purchase")
        instance.delete()


    @item_swagger("Get all purchase", "Purchase", method="GET")
    def list(self, request, *args, **kwargs):
        """
        Supports ?search=keyword and ?pay_status=True filters
        """
        return super().list(request, *args, **kwargs)

    @item_swagger("Get a single purchase", "Purchase", method="GET")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @item_swagger("Create new purchase", "Purchase", requestdata=PurchaseSerializer, method="POST")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @item_swagger("Update purchase", "Purchase", requestdata=PurchaseSerializer, method="PUT")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @item_swagger("Delete purchase", "Purchase", method="DELETE")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_200_OK)
    

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']
    def get_queryset(self):
        today = timezone.localdate()
        if self.request.user.is_superuser:
            return SaleProduct.objects.filter(create_date__date=today).order_by('-id')
        return SaleProduct.objects.filter(user=self.request.user, create_date__date=today).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and serializer.instance.user != self.request.user :
            raise PermissionDenied("You cannot update another user's Sale")        
        serializer.save(user=serializer.instance.user)

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.user != self.request.user:
            raise PermissionDenied("You cannot delete another user's Sale")
        instance.delete()
    

    @item_swagger("Get all sale", "Sale", method="GET")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @item_swagger("Get a single sale", "Sale", method="GET")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @item_swagger("Create new sale", "Sale", requestdata=SaleSerializer, method="POST")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @item_swagger("Update sale", "Sale", requestdata=SaleSerializer, method="PUT")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @item_swagger("Delete sale", "Sale", method="DELETE")
    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"detail": "Deleted successfully."},
                status=status.HTTP_200_OK
            )


class WorkLogSetView(viewsets.ModelViewSet):
    serializer_class = WorkLogSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post']

    def get_queryset(self):
        queryset = WorkLog.objects.all()  # ✅ fix here
        user_id = self.request.query_params.get("user_id")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @swagger_auto_schema(
        tags=['Workload'],
        operation_summary="Get all worklogs",
        operation_description="Retrieve worklogs. Superusers can use ?user_id=<id> to filter by user.",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Bearer access token (e.g. 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="Filter by user ID (superuser only)",
                type=openapi.TYPE_INTEGER,
                required=False,  # ✅ optional
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @item_swagger("Post a single workload", "Workload", requestdata=WorkLogSerializer,method="POST")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @item_swagger("Post a single workload", "Workload", requestdata=WorkLogSerializer,method="Put")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)




