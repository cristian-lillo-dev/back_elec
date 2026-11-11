from django.db import models
from .temas import Tema

class Tema(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=1)
    bandera = models.IntegerField(default=1)

    class Meta:
        db_table = 'tema'
        ordering = ['orden']
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'

    def __str__(self):
        return f"{self.orden}. {self.nombre}"