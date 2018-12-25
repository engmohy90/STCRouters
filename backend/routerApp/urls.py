"""routers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RouterViewSet, SlotViewSet, PortViewSet, NeighborViewSet

router = DefaultRouter()
router.register(prefix='router', viewset=RouterViewSet)
router.register(prefix='slot', viewset=SlotViewSet)
router.register(prefix='port', viewset=PortViewSet)
router.register(prefix='neighbor', viewset=NeighborViewSet)

urlpatterns = [
    path(r'api/', include(router.urls)),
]
