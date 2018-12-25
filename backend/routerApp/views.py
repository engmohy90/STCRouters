from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import Port, Slot, Router, Neighbor
from .serializers import PortSerializer, SlotSerializer, RouterSerializer, NeighborSerializer


class RouterViewSet(ModelViewSet):
    queryset = Router.objects.all()
    serializer_class = RouterSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name',)


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'router',)


class PortViewSet(ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('router', 'slot', 'name',)


class NeighborViewSet(ModelViewSet):
    queryset = Neighbor.objects.all()
    serializer_class = NeighborSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('router', 'remote',)
