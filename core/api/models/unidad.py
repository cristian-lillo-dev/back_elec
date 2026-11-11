from django.db import models

class Unidad(models.Model):
    tema = models.ForeignKey(
        Tema, 
        on_delete=models.CASCADE, 
        related_name='unidades',
        verbose_name='Tema'
    )
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    pdf_url = models.URLField(max_length=500, blank=True, null=True)
    orden = models.IntegerField(default=1)

    class Meta:
        db_table = 'unidad'
        ordering = ['orden']
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return f"{self.orden}. {self.nombre}"