from django.db import models
from django.utils import timezone
from .perfil import PerfilUsuario


class Transaccion(models.Model):
    usuario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.CASCADE,
        related_name='transacciones'
    )
    tipo_movimiento = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=255)
    moneda_origen = models.CharField(max_length=50, default='CLP')
    pasarela_pago = models.CharField(max_length=100, default='Webpay')
    numero_cuenta_destino = models.CharField(max_length=100, blank=True, null=True)
    empresa_destino = models.CharField(max_length=150, blank=True, null=True)
    referencia_externa = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'transaccion'
        ordering = ['-fecha']
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

    def __str__(self):
        return f"{self.usuario.user.username} - {self.tipo_movimiento}: {self.cantidad}"