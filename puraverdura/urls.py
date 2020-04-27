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
from django.contrib import admin
import juntagrico

# Custom Views of Pura Verdura
from puraverdura import views as puraverdura

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('juntagrico.urls')),
    url(r'^$', juntagrico.views.home),
    url(r'^impersonate/', include('impersonate.urls')),

    # stats
    url('stats/', puraverdura.stats),

    # pdf (override)
    url('my/pdf/depotlist', puraverdura.depot_list),
    url('my/pdf/depotoverview', puraverdura.depot_overview),
    url('my/pdf/amountoverview', puraverdura.amount_overview),
]
