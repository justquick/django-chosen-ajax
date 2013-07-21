from django.db import models


class Pony(models.Model):
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)

    class Meta:
        db_table = 'chosen_pony'

    def __unicode__(self):
        return self.name

