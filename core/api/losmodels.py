# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone


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


class Unidad(models.Model):
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