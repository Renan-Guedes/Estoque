from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]