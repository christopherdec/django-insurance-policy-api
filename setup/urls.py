from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from policies.views import PolicyViewSet

router = DefaultRouter()
router.register(r'policies', PolicyViewSet, basename='policies')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
