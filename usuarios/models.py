
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class CodigoAcceso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    generado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    ROLES = (
        ('admin', 'Administrador'),
        ('editor', 'Editor'),
        ('periodista', 'Periodista'),
    )

    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"
    
class Video(models.Model):



    titulo = models.CharField(max_length=200)
    categorias = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField()
    ## archivo = models.FileField(upload_to='videos/')
    archivo = models.FileField(upload_to='multimedia/')
    tipo = models.CharField(max_length=10, choices=[
        ('video', 'Video'),
        ('imagen', 'Imagen')
    ],
    default='video'
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    ##titulo = models.CharField(max_length=255)
    ##descripcion = models.TextField()
    ##fecha_subida = models.DateTimeField(auto_now_add=True)

    

    tipo = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return self.titulo    