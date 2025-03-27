from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include(('news.urls', 'news'), namespace='news')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
]
