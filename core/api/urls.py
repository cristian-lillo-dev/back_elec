from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnidadViewSet, LeccionViewSet, PaginaLeccionViewSet,
    ContenidoLeccionViewSet, PreguntaLeccionViewSet,
    OpcionPreguntaLeccionViewSet, PerfilUsuarioViewSet,
    ProgresoUsuarioViewSet, TransaccionViewSet
)

router = DefaultRouter()
router.register(r'unidades', UnidadViewSet, basename='unidad')
router.register(r'lecciones', LeccionViewSet, basename='leccion')
router.register(r'paginas', PaginaLeccionViewSet, basename='pagina')
router.register(r'contenidos', ContenidoLeccionViewSet, basename='contenido')
router.register(r'preguntas', PreguntaLeccionViewSet, basename='pregunta')
router.register(r'opciones', OpcionPreguntaLeccionViewSet, basename='opcion')
router.register(r'perfiles', PerfilUsuarioViewSet, basename='perfil')
router.register(r'progresos', ProgresoUsuarioViewSet, basename='progreso')
router.register(r'transacciones', TransaccionViewSet, basename='transaccion')

urlpatterns = [
    path('', include(router.urls)),
]