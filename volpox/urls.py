from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'volpox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('seguridad.urls',namespace='seguridad')),
    url(r'^localizacion/', include('localizacion.urls',namespace='localizacion')),
    url(r'^regional/', include('regional.urls',namespace='regional')),
    url(r'^nacional/', include('nacional.urls',namespace='nacional')),
]
