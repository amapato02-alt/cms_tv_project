
# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import CodigoAcceso, PerfilUsuario
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import PerfilUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Video
from .forms import VideoForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VideoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Video
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt




def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            codigo = form.cleaned_data['codigo']
            codigo_obj = CodigoAcceso.objects.get(codigo=codigo)

            codigo_obj.usado = True
        
            codigo_obj.save()

            PerfilUsuario.objects.create(
                usuario=user,
                rol='periodista'
            )

            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            perfil = PerfilUsuario.objects.get(usuario=user)

            if perfil.rol == 'admin':
                return redirect('panel_admin')
            elif perfil.rol == 'editor':
                return redirect('panel_editor')
            else:
                return redirect('panel_periodista')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')



@login_required
def panel_admin(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)
    videos = Video.objects.all()
    if perfil.rol != 'admin':
        return redirect('login')
    

    ##videos = Video.objects.filter(usuario=request.user)

    query = request.GET.get('q')
    fecha = request.GET.get('fecha')
    categorias = request.GET.getlist('categoria')

    # 🔍 BUSQUEDA POR TITULO O DESCRIPCIÓN
    if query:
        videos = videos.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    

    # 📅 FILTRO POR FECHA
    if fecha:
        videos = videos.filter(fecha_subida__date=fecha)

    if categorias:
        query_categoria = Q()
        for cat in categorias:
            query_categoria |= Q(categorias__icontains=cat)

        videos = videos.filter(query_categoria)

    # 📌 ORDENAR (opcional pero recomendado)
    videos = videos.order_by('-fecha_subida')



    return render(request, 'admin_panel.html', {'videos': videos})

@login_required
def panel_editor(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if perfil.rol != 'editor':
        return redirect('login')

    return render(request, 'editor_panel.html')

@login_required
def panel_periodista(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if perfil.rol != 'periodista':
        return redirect('login')


    videos = Video.objects.filter(usuario=request.user)

    query = request.GET.get('q')
    fecha = request.GET.get('fecha')
    categorias = request.GET.getlist('categoria')

    # 🔍 BUSQUEDA POR TITULO O DESCRIPCIÓN
    if query:
        videos = videos.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )

    

    # 📅 FILTRO POR FECHA
    if fecha:
        videos = videos.filter(fecha_subida__date=fecha)

    if categorias:
        query_categoria = Q()
        for cat in categorias:
            query_categoria |= Q(categorias__icontains=cat)

        videos = videos.filter(query_categoria)

    # 📌 ORDENAR (opcional pero recomendado)
    videos = videos.order_by('-fecha_subida')

    return render(request, 'periodista_panel.html', {'videos': videos})

    ##return render(request, 'periodista_panel.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#@login_required
#def subir_video(request):
   # if request.method == 'POST':
   #     form = VideoForm(request.POST, request.FILES)

  #      if form.is_valid():
 #           video = form.save(commit=False)
           # video.usuario = request.user
            
          #  categorias = request.POST.getlist('categorias')
         #   video.categorias = ','.join(categorias)

        #    video.save()

            # Redirigir según rol
       #     if request.user.is_staff:
      #          return redirect('panel_admin')
     #       else:
    #            return redirect('panel_periodista')

            ##return redirect('panel_periodista')
            
   # else:
  #      form = VideoForm()


        
         

 #   return render(request, 'subir_video.html', {'form': form})


@login_required
def subir_video(request):

    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save(commit=False)
            video.usuario = request.user
            
            categorias = request.POST.getlist('categorias')
            video.categorias = ','.join(categorias)

            video.save()

            # 🔥 REDIRECCIÓN CORRECTA SEGÚN TU SISTEMA
            if perfil.rol == 'admin':
                return redirect('panel_admin')
            elif perfil.rol == 'editor':
                return redirect('panel_editor')
            else:
                return redirect('panel_periodista')

    else:
        form = VideoForm()

    return render(request, 'subir_video.html', {'form': form})



##@login_required
##def lista_videos(request):
  ##  videos = Video.objects.all().order_by('-fecha_subida')
  ##  return render(request, 'lista_videos.html', {'videos': videos})

@login_required
def lista_videos(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if perfil.rol == 'admin':
        videos = Video.objects.all()
    else:
        videos = Video.objects.filter(usuario=request.user)

    return render(request, 'lista_videos.html', {'videos': videos})

@login_required
def editar_video(request, id):
    ##video = Video.objects.get(id=id)

    # Seguridad
    ##if video.usuario != request.user:
    ##    return redirect('lista_videos')
    
    video = Video.objects.get(id=id)
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if perfil.rol != 'admin' and video.usuario != request.user:
        return redirect('lista_videos')

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)

        categorias = request.POST.getlist('categorias')
        video.categorias = ','.join(categorias)

        if form.is_valid():
            form.save()
            ##return redirect('panel_periodista')
        if perfil.rol == 'admin':
            return redirect('panel_admin')
        else:
            return redirect('panel_periodista')
    else:
        form = VideoForm(instance=video)

    

    return render(request, 'editar_video.html', {'form': form})

@login_required
def eliminar_video(request, id):
    ##video = Video.objects.get(id=id)

    ##if video.usuario != request.user:
      ##  return redirect('lista_videos')
    
    video = Video.objects.get(id=id)
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if perfil.rol != 'admin' and video.usuario != request.user:
        return redirect('lista_videos')

    video.delete()
    ##return redirect('panel_periodista')
    if perfil.rol == 'admin':
        return redirect('panel_admin')
    else:
        return redirect('panel_periodista')

@api_view(['GET'])
def api_videos(request):
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)
  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_subir_video(request):
    serializer = VideoSerializer(data=request.data)

    if serializer.is_valid():
       ## serializer.save(usuario=request.user)
        archivo = request.FILES.get('archivo')

    if archivo.content_type.startswith('video'):
        tipo = 'video'
    elif archivo.content_type.startswith('image'):
        tipo = 'imagen'
    else:
        tipo = 'otro'

    serializer.save(usuario=request.user, tipo=tipo)

    return Response(serializer.errors)

@login_required
def mis_videos(request):
    videos = Video.objects.filter(usuario=request.user)
    return render(request, 'videos/mis_videos.html', {'videos': videos})