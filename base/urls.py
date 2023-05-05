from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('', views.Base.as_view(), name='home'),
    path('edit/<int:id>/', views.EditTask.as_view(), name='edit')
]