import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=False)
    price = models.FloatField(blank=False)
    url = models.URLField(max_length=300, blank=False)
