

# Register your models here.
from django.contrib import admin
from .models import CodigoAcceso, PerfilUsuario
from .models import Video
from django.shortcuts import redirect

admin.site.register(CodigoAcceso)
admin.site.register(PerfilUsuario)
admin.site.register(Video)

