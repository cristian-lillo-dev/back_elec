from django.db import models
from .leccion import Leccion


class PreguntaLeccion(models.Model):
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='preguntas'
    )
    texto = models.TextField()
    tipo = models.CharField(max_length=50, default='multiple_choice')
    respuesta_texto = models.TextField(blank=True, null=True)
    extracto_referencia = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=1)

    class Meta:
        db_table = 'pregunta_leccion'
        ordering = ['orden']
        verbose_name = 'Pregunta de Lección'
        verbose_name_plural = 'Preguntas de Lección'

    def __str__(self):
        return f"P{self.orden}: {self.texto[:40]}"


class OpcionPreguntaLeccion(models.Model):
    pregunta_leccion = models.ForeignKey(
        PreguntaLeccion,
        on_delete=models.CASCADE,
        related_name='opciones'
    )
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    class Meta:
        db_table = 'opcion_pregunta_leccion'
        verbose_name = 'Opción de Pregunta'
        verbose_name_plural = 'Opciones de Preguntas'

    def __str__(self):
        return f"{'[✓]' if self.es_correcta else '[ ]'} {self.texto[:30]}"