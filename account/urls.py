from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from account import views
app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.conta, name='profile'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('login/', LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('pass_recovery/', views.pass_recovery, name='pass_recovery'),

]