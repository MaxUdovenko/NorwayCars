from django.contrib import admin
from django.urls import path, include

from ploting import views as pl

urlpatterns = [
    path('', pl.pandas_table, name='index'),
    path('admin/', admin.site.urls),
    path('pandas/', include('ploting.urls')),
]
