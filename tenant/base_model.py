from django.db import models


class BaseModel(models.Model):
    organization = models.ForeignKey('tenant.Organization', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
