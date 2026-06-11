##from django.urls import path
##from .views import registro

##urlpatterns = [
##    path('registro/', registro, name='registro'),
##]

from django.urls import path
from .views import registro, login_view, logout_view
from .views import panel_admin, panel_editor, panel_periodista
from .views import subir_video, lista_videos
from .views import editar_video, eliminar_video
from .views import api_videos, api_subir_video
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'), 
    path('admin-panel/', panel_admin, name='panel_admin'),
    path('editor-panel/', panel_editor, name='panel_editor'),
    path('periodista-panel/', panel_periodista, name='panel_periodista'),
    path('logout/', logout_view, name='logout'),
    path('subir-video/', subir_video, name='subir_video'),
    path('videos/', lista_videos, name='lista_videos'),
    path('editar-video/<int:id>/', editar_video, name='editar_video'),
    path('eliminar-video/<int:id>/', eliminar_video, name='eliminar_video'),
    path('api/videos/', api_videos),
    path('api/subir-video/', api_subir_video),

    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ),
    name='password_reset'
),

path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ),
    name='password_reset_done'
),

path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ),
    name='password_reset_complete'
),
    
]