from django.db import models


class Router(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    """
    every router has 8 slot unique with router
    """
    name = models.CharField(max_length=200)
    router = models.ForeignKey('Router', on_delete=models.CASCADE, )
    node_type = models.CharField(max_length=200)
    speed = models.CharField(max_length=200)
    port_count = models.IntegerField()
    state = models.CharField(max_length=200)

    class Meta:
        unique_together = ('name', 'router',)

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=200)
    router = models.ForeignKey('Router', on_delete=models.CASCADE, )
    slot = models.ForeignKey('Slot', on_delete=models.CASCADE, )
    ip = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    class Meta:
        unique_together = ('name', 'router', 'slot')

    def __str__(self):
        return self.name


class Neighbor(models.Model):
    router = models.ForeignKey('Router', on_delete=models.CASCADE, )
    remote = models.CharField(max_length=200)
    # router_port = models.ForeignKey('Port', on_delete=models.CASCADE, )
    router_port = models.CharField(max_length=200)
    remote_port = models.CharField(max_length=200)
    router_slot = models.CharField(max_length=200)
    remote_slot = models.CharField(max_length=200)

    def __str__(self):
        return f"Neighbor For {self.router.name}"
