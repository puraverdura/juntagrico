"""puraverdura URL Configuration

The `urlpatterns` list routes URLs to views. 
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
import juntagrico

# Custom Views of Pura Verdura
from puraverdura import views as puraverdura
#from puraverdura import views_admin as puraverdura_admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('juntagrico.urls')),
    url(r'^$', juntagrico.views.home),
    url(r'^impersonate/', include('impersonate.urls')),

    # stats
    url('stats/', puraverdura.stats),

    # pdf (override)
    # path('my/pdf/depotlist/', puraverdura.depot_list, name='depot_list'),
    # url('my/pdf/depotoverview', puraverdura.depot_overview),
    # url('my/pdf/amountoverview', puraverdura.amount_overview),

    # member email list
    path('my/filters_emails/', puraverdura.filters_emails, name='filters_emails'),

    # tutorial section
    path('my/tutorials/', puraverdura.tutorials, name='tutorials'),

    # override profile (trailing forward slach is important)
    path('my/profile/', puraverdura.profile, name='profile'),

    #path('my/mails/send/depot/', puraverdura_admin.send_email_depot, name='mail-depot-send'),
    #path('my/mails/send/area/', puraverdura_admin.send_email_area, name='mail-area-send'),
    #path('my/mails/send/', puraverdura_admin.send_email, name='mail-send'),  
    ]