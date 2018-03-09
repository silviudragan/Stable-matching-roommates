from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from stable import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('stable.urls')),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^ajax/validate_username/$', views.display_info_coleg, name='display_info_coleg'),
    url(r'^ajax/recenzii_facute/$', views.recenzii_facute, name='recenzii_facute'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
