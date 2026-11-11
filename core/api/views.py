from rest_framework import viewsets, filters
from .models import (
    PerfilUsuario, Unidad, Leccion, PaginaLeccion,
    ContenidoLeccion, PreguntaLeccion, OpcionPreguntaLeccion,
    ProgresoUsuario, Transaccion
)
from .serializers import (
    PerfilUsuarioSerializer, UnidadSerializer, LeccionSerializer,
    PaginaLeccionSerializer, ContenidoLeccionSerializer,
    PreguntaLeccionSerializer, OpcionPreguntaLeccionSerializer,
    ProgresoUsuarioSerializer, TransaccionSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import PerfilUsuarioSerializer

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all().prefetch_related('lecciones')
    serializer_class = UnidadSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['orden', 'nombre']


class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.all().prefetch_related(
        'paginas_detalle__contenidos',
        'preguntas__opciones'
    )
    serializer_class = LeccionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['orden']

    def get_queryset(self):
        queryset = super().get_queryset()
        unidad_id = self.request.query_params.get('unidad_id')
        if unidad_id:
            queryset = queryset.filter(unidad_id=unidad_id)
        return queryset


class PaginaLeccionViewSet(viewsets.ModelViewSet):
    queryset = PaginaLeccion.objects.all().prefetch_related('contenidos')
    serializer_class = PaginaLeccionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        leccion_id = self.request.query_params.get('leccion_id')
        if leccion_id:
            queryset = queryset.filter(leccion_id=leccion_id)
        return queryset


class ContenidoLeccionViewSet(viewsets.ModelViewSet):
    queryset = ContenidoLeccion.objects.all()
    serializer_class = ContenidoLeccionSerializer


class PreguntaLeccionViewSet(viewsets.ModelViewSet):
    queryset = PreguntaLeccion.objects.all().prefetch_related('opciones')
    serializer_class = PreguntaLeccionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        leccion_id = self.request.query_params.get('leccion_id')
        if leccion_id:
            queryset = queryset.filter(leccion_id=leccion_id)
        return queryset


class OpcionPreguntaLeccionViewSet(viewsets.ModelViewSet):
    queryset = OpcionPreguntaLeccion.objects.all()
    serializer_class = OpcionPreguntaLeccionSerializer


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all().select_related('user').prefetch_related('progresos', 'transacciones')
    serializer_class = PerfilUsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email']


class ProgresoUsuarioViewSet(viewsets.ModelViewSet):
    queryset = ProgresoUsuario.objects.all()
    serializer_class = ProgresoUsuarioSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        return queryset


class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)
        return queryset



@api_view(['POST'])
def api_login(request):
    print("LLEGUE AL LOGIN")
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Autenticamos contra la tabla auth_user de Django
    user = authenticate(username=username, password=password)
    
    if user is not None:
        try:
            # Obtenemos el perfil asociado usando el OneToOneField
            perfil = user.perfil 
            serializer = PerfilUsuarioSerializer(perfil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "El usuario existe pero no tiene un perfil asociado."}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)