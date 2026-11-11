from django.db import models
from .perfil import PerfilUsuario
from .leccion import Leccion


class ProgresoUsuario(models.Model):
    usuario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name='progresos'
    )
    leccion = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name='progresos_usuarios'
    )
    porcentaje_avance = models.FloatField(default=0.0)
    estado = models.CharField(max_length=50, default='no_iniciado')

    class Meta:
        db_table = 'progreso_usuario'
        unique_together = ('usuario', 'leccion')
        verbose_name = 'Progreso de Usuario'
        verbose_name_plural = 'Progresos de Usuarios'

    def __str__(self):
        return f"{self.usuario.user.username} - {self.leccion.nombre} ({self.porcentaje_avance}%)"