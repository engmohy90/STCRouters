from django.forms.models import model_to_dict
from rest_framework import serializers

from .models import Port, Slot, Router, Neighbor


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = ("__all__")


class SlotSerializer(serializers.ModelSerializer):
    ports = serializers.SerializerMethodField()
    router = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ("__all__")

    def get_ports(self, obj):
        if obj.id and obj.router:
            ports = Port.objects.filter(router=obj.router, slot=obj)
            return PortSerializer(ports, many=True).data
        else:
            return ""

    def get_router(self, obj):

        if obj.router:
            return model_to_dict(obj.router)
        else:
            return ""


class PortSerializer(serializers.ModelSerializer):
    remote_router = serializers.SerializerMethodField()

    class Meta:
        model = Port
        fields = ("__all__")

    def get_remote_router(self, obj):
        remote_router_query = Neighbor.objects.filter(
            router=obj.router, router_port=obj.name, router_slot=obj.slot.name)
        if remote_router_query:
            remote_id = Router.objects.filter(name=remote_router_query[0].remote)
            return RouterSerializer(remote_id, many=True).data
        else:
            return ""


class NeighborSerializer(serializers.ModelSerializer):
    router_name = serializers.CharField(source='router.name', read_only=True)

    class Meta:
        model = Neighbor
        fields = ("__all__")
