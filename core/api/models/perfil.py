from django.db import models
from django.conf import settings


class PerfilUsuario(models.Model):
    """
    Extensión del modelo User nativo de Django (relación 1 a 1).
    Hereda username, password, email, first_name, last_name del auth.User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    categoria = models.CharField(max_length=100, default='Estudiante SEC')
    monedas = models.IntegerField(default=0)
    vidas = models.IntegerField(default=5)

    class Meta:
        db_table = 'perfil_usuario'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __str__(self):
        return f"{self.user.username} - {self.categoria}"