from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    PerfilUsuario, Unidad, Leccion, PaginaLeccion, 
    ContenidoLeccion, PreguntaLeccion, OpcionPreguntaLeccion,
    ProgresoUsuario, Transaccion
)

# Integrar perfil de vidas/monedas en la ficha del User de Django
class PerfilInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Juego (Vidas y Monedas)'

class CustomUserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Configuración de Contenidos y Preguntas
class OpcionInline(admin.TabularInline):
    model = OpcionPreguntaLeccion
    extra = 4

@admin.register(PreguntaLeccion)
class PreguntaAdmin(admin.ModelAdmin):
    inlines = [OpcionInline]
    list_display = ('orden', 'texto', 'leccion', 'tipo')
    list_filter = ('leccion', 'tipo')

class ContenidoInline(admin.StackedInline):
    model = ContenidoLeccion
    extra = 1

@admin.register(PaginaLeccion)
class PaginaAdmin(admin.ModelAdmin):
    inlines = [ContenidoInline]
    list_display = ('leccion', 'numero_pagina')

admin.site.register(Unidad)
admin.site.register(Leccion)
admin.site.register(ProgresoUsuario)
admin.site.register(Transaccion)