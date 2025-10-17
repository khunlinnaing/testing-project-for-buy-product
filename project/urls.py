from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

schema_view = get_schema_view(
   openapi.Info(
      title="Mini POS",
      default_version='v1',
      description="API documentation using Swagger",
      terms_of_service="https://www.linkedin.com/in/khun-lin-naing-oo-4272a4255/",
      contact=openapi.Contact(email="khunlinnaing90@email.com"),
      license=openapi.License(name="KLNO License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('user', UserProfileViewSet)
router.register('purchase', PurchaseViewSet, basename='purchase')
router.register('sale', SaleViewSet, basename='sale')
router.register('worklog', WorkLogSetView, basename='worklog')

def dummy_login_view(request):
    return JsonResponse({
        "error": "This is an API-only app. Please use /api/login/ instead."
    }, status=400)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),

    # add this to silence reverse('login') errors
    path('login/', dummy_login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('', include(router.urls)),
]
