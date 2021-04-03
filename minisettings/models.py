from django.db import models


class MiniSetting(models.Model):
    TYPES = (
        (1, 'Boolean'),
        (2, 'Integer'),
        (3, 'Float'),
        (4, 'String')
        )
    
    name = models.CharField(max_length=250)
    type = models.PositiveIntegerField(choices=TYPES)
    value = models.CharField(max_length=250)
