from django.contrib import admin
from django.urls import path, include
from esppedu.revista import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
   # path('upload/', views.upload, name='upload'),
    path('artigos/', views.artigos_lista, name='artigo_lista'),
    path('artigos/<int:pk>/', views.artigos_delete, name='artigo_delete'),
    path('artigos/upload', views.artigos_upload, name='artigo_upload'),
    path('signup/', views.signup, name='signup'),
    path('secret/', views.secret_page, name='secret'),
    path('secret2/', views.SecretPage.as_view(), name='secret2'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
