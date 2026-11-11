from django.db import models
from .unidad import Unidad


class Leccion(models.Model):
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.CASCADE,
        related_name='lecciones'
    )
    nombre = models.CharField(max_length=255)
    paginas = models.IntegerField(default=0)
    modo = models.CharField(max_length=50, default='estudio')
    orden = models.IntegerField(default=1)

    class Meta:
        db_table = 'leccion'
        ordering = ['orden']
        verbose_name = 'Lección'
        verbose_name_plural = 'Lecciones'

    def __str__(self):
        return f"{self.unidad.nombre} - {self.nombre}"


class PaginaLeccion(models.Model):
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='paginas_detalle'
    )
    numero_pagina = models.IntegerField()

    class Meta:
        db_table = 'pagina_leccion'
        ordering = ['numero_pagina']
        unique_together = ('leccion', 'numero_pagina')
        verbose_name = 'Página de Lección'
        verbose_name_plural = 'Páginas de Lección'

    def __str__(self):
        return f"{self.leccion.nombre} - Pág {self.numero_pagina}"


class ContenidoLeccion(models.Model):
    pagina_leccion = models.ForeignKey(
        PaginaLeccion,
        on_delete=models.CASCADE,
        related_name='contenidos'
    )
    texto = models.TextField()

    class Meta:
        db_table = 'contenido_leccion'
        verbose_name = 'Contenido de Lección'
        verbose_name_plural = 'Contenidos de Lección'

    def __str__(self):
        return f"Texto Pág {self.pagina_leccion.numero_pagina}: {self.texto[:30]}..."