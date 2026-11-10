from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    PerfilUsuario, Unidad, Leccion, PaginaLeccion,
    ContenidoLeccion, PreguntaLeccion, OpcionPreguntaLeccion,
    ProgresoUsuario, Transaccion
)

# -------------------------------------------------------------------------
# 1. Serializadores de Contenido y Lección
# -------------------------------------------------------------------------

class ContenidoLeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContenidoLeccion
        fields = ['id', 'pagina_leccion', 'texto']


class PaginaLeccionSerializer(serializers.ModelSerializer):
    contenidos = ContenidoLeccionSerializer(many=True, read_only=True)

    class Meta:
        model = PaginaLeccion
        fields = ['id', 'leccion', 'numero_pagina', 'contenidos']


# -------------------------------------------------------------------------
# 2. Serializadores de Preguntas y Evaluación (Escritura anidada habilitada)
# -------------------------------------------------------------------------

class OpcionPreguntaLeccionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = OpcionPreguntaLeccion
        fields = ['id', 'pregunta_leccion', 'texto', 'es_correcta']
        extra_kwargs = {'pregunta_leccion': {'required': False}}


class PreguntaLeccionSerializer(serializers.ModelSerializer):
    opciones = OpcionPreguntaLeccionSerializer(many=True, required=False)

    class Meta:
        model = PreguntaLeccion
        fields = [
            'id',
            'leccion',
            'texto',
            'tipo',
            'respuesta_texto',
            'extracto_referencia',
            'orden',
            'opciones'
        ]

    def create(self, validated_data):
        opciones_data = validated_data.pop('opciones', [])
        pregunta = PreguntaLeccion.objects.create(**validated_data)
        for opcion_data in opciones_data:
            OpcionPreguntaLeccion.objects.create(pregunta_leccion=pregunta, **opcion_data)
        return pregunta

    def update(self, instance, validated_data):
        opciones_data = validated_data.pop('opciones', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if opciones_data is not None:
            existing_ids = [op.id for op in instance.opciones.all()]
            sent_ids = [op.get('id') for op in opciones_data if op.get('id') is not None]

            # Eliminar opciones borradas en el frontend
            for existing_id in existing_ids:
                if existing_id not in sent_ids:
                    OpcionPreguntaLeccion.objects.filter(id=existing_id).delete()

            # Crear o actualizar opciones
            for opcion_data in opciones_data:
                opcion_id = opcion_data.get('id')
                if opcion_id:
                    OpcionPreguntaLeccion.objects.filter(id=opcion_id).update(**opcion_data)
                else:
                    OpcionPreguntaLeccion.objects.create(pregunta_leccion=instance, **opcion_data)

        return instance


# -------------------------------------------------------------------------
# 3. Serializadores de Módulos (Lección y Unidad)
# -------------------------------------------------------------------------

class LeccionSerializer(serializers.ModelSerializer):
    paginas_detalle = PaginaLeccionSerializer(many=True, read_only=True)
    preguntas = PreguntaLeccionSerializer(many=True, read_only=True)

    class Meta:
        model = Leccion
        fields = [
            'id',
            'unidad',
            'nombre',
            'paginas',
            'modo',
            'orden',
            'paginas_detalle',
            'preguntas'
        ]


class UnidadSerializer(serializers.ModelSerializer):
    lecciones = LeccionSerializer(many=True, read_only=True)

    class Meta:
        model = Unidad
        fields = [
            'id',
            'nombre',
            'descripcion',
            'pdf_url',
            'orden',
            'lecciones'
        ]


# -------------------------------------------------------------------------
# 4. Progreso y Transacciones
# -------------------------------------------------------------------------

class ProgresoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoUsuario
        fields = '__all__'


class TransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaccion
        fields = '__all__'


# -------------------------------------------------------------------------
# 5. Usuario y Perfil 1 a 1 (Con soporte robusto de escritura anidada)
# -------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    progresos = ProgresoUsuarioSerializer(many=True, read_only=True)
    transacciones = TransaccionSerializer(many=True, read_only=True)

    class Meta:
        model = PerfilUsuario
        fields = [
            'id',
            'user',
            'categoria',
            'monedas',
            'vidas',
            'progresos',
            'transacciones'
        ]

    def create(self, validated_data):
        # Extraemos los datos del usuario enviados desde la petición
        user_data = validated_data.pop('user', None)
        if not user_data:
            raise serializers.ValidationError({"user": "Los datos del usuario son obligatorios."})

        password = user_data.pop('password', None)

        # Creamos el usuario asegurando el uso de create_user para hashear la contraseña correctamente
        user = User.objects.create_user(password=password, **user_data)

        # Creamos el perfil vinculado al usuario recién creado
        perfil = PerfilUsuario.objects.create(user=user, **validated_data)
        return perfil