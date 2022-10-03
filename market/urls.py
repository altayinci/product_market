from django.contrib import admin
from django.urls import path, include

from rest_framework import routers, permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from product_api.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename="products")

schema_view = get_schema_view(
   openapi.Info(
      title="Products API",
      default_version='v1',
      description="Product Listing",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]

urlpatterns += [
   path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]