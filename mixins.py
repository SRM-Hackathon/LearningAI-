from django.db import models


class TimeStampMixin(models.Model):

    utc_update = models.DateTimeField(auto_now=True)
    utc_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
