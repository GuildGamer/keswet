from django.urls import path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("manage", views.UserViewSet, basename="manage")
router.register("auth", views.UserAuthViewSet, basename="auth")

app_name = "accounts"

urlpatterns = []

urlpatterns += router.urls
