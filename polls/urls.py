from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

App_name ="polls"

urlpatterns = [
  path('', views.index, name="index"),
  path('login/', views.login_view, name="login"),
  path('logout/', views.logout_view, name="logout"),
  #path('register/', views.register_fingerprint, name='register_fingerprint'),
  path('addcandidate/', views.addcandidate_view, name="candidates"),
  path('addelection/', views.addelection_view, name="election"),
  path('saddvoter/', views.addvoter_view, name="voters"),
  path('results/', views.result_view, name="result")
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
