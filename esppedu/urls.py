from django.contrib import admin
from django.urls import path, include
from esppedu.revista import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url



urlpatterns = [
    path('', views.home, name='home'),

    path('upload/', views.artigos_upload, name='upload'),
    path('artigos/', views.artigos_lista, name='artigo_lista'),
    path('artigos/<int:pk>/', views.artigos_delete, name='artigo_delete'),
    path('artigos/upload', views.artigos_upload, name='artigo_upload'),
    #path('signup', views.signup, name='signup'),
    
    path('accounts', include('django.contrib.auth.urls')),
    path('admin', admin.site.urls),

    path('signup/', views.signup_view, name="signup"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
