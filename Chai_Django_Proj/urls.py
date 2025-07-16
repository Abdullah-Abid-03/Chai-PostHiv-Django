"""
URL configuration for Chai_Django_Proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Chai_Django_Proj import Views
from django.conf import settings  # for media files.#
from django.conf.urls.static import static  # for media files.#
from django.conf import urls as conf_urls  # for handling error pages
import posts  # b/c the views  are in the posts app

handler404 = 'posts.views.custom_404_view'
handler500 = 'posts.views.custom_500_view'

urlpatterns = [  # at project level
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),  # this will now catch all the app-level paths correctly.
    # That’s it. One line to include everything from posts/urls.py.
    # That tell Django that doesn’t match admin/, look into posts.urls and see if it matches something there
    path('tinymce/', include('tinymce.urls')),
]
# serves during development
if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Serve media when DEBUG=False
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static only when DEBUG = False
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


