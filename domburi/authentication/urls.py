from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('login/', views.AuthenticationUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUserView.as_view(), name='profile'),
    path('about-me/', views.AboutMeView.as_view(), name='about_me'),

    path('session/get', views.get_session_view, name='session_get'),
    path('session/set', views.set_session_view, name='session_set'),
]
