from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from stable import views
from stable import administrator

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('stable.urls')),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^resetPass/$', views.ResetPass.as_view(), name='resetPass'),
    url(r'^administrator/$', administrator.Administrator.as_view(), name='administrator'),
    url(r'^administrator/resetare/$', administrator.Resetare.as_view(), name='resetare'),
    url(r'^administrator/avansare/$', administrator.Avansare.as_view(), name='avansare'),
    url(r'^administrator/excel/$', administrator.GenerareExcel.as_view(), name='excel'),
    url(r'^administrator/camin/$', administrator.StatisticaCamine.as_view(), name='camin'),
    url(r'^administrator/cont/$', administrator.CreareConturi.as_view(), name='cont'),
    url(r'^ajax/validate_username/$', views.display_info_coleg, name='display_info_coleg'),
    url(r'^ajax/recenzii_facute/$', views.recenzii_facute, name='recenzii_facute'),
    url(r'^ajax/recenzii_primite/$', views.recenzii_primite, name='recenzii_primite'),
    url(r'^ajax/toate_recenziile/$', views.toate_recenziile, name='toate_recenziile'),
    url(r'^ajax/preferinte_student/$', views.preferinte_student, name='preferinte_student'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
