from django.urls import path
from . import views
from .views import EditProfile

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/<uuid:id>/', views.profile, name='profile'),
    path('update/profile/<uuid:id>/', views.EditProfile.as_view(), name='edit_profile'),
]