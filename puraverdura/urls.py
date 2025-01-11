"""demo URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

import juntagrico

# Import custom views of Pura Verdura that are decalred in views.py
from puraverdura import views as puraverdura
from puraverdura import views_subscription as puraverdura_subscription
from puraverdura import views_admin as puraverdura_admin


urlpatterns = [
    path(r'admin/shell/', include('django_admin_shell.urls')),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^impersonate/', include('impersonate.urls')),
    re_path(r'^djrichtextfield/', include('djrichtextfield.urls')),

    # Import Juntagrico URLs
    re_path(r'^', include('juntagrico.urls')),
    re_path(r'^$', juntagrico.views.home),
    path('badges/', include('juntagrico_badges.urls')),
    re_path(r'^', include('juntagrico_pg.urls')),

    # Add Custom Puraverdura views
    # member email list
    path('my/filters_emails/', puraverdura.filters_emails, name='filters_emails'),

    # tutorial section
    path('my/tutorials/', puraverdura.tutorials, name='tutorials'),

    # Override Juntagrico views
    # override share certificate
    path('my/share/certificate/', puraverdura_subscription.share_certificate, name='share-certificate'),

    # override subscription cancellation
    path('my/subscription/cancel/<int:subscription_id>', puraverdura_subscription.cancel_subscription,
         name='sub-cancel'),

    # override membership cancellation
    path('my/cancel/membership/', puraverdura.cancel_membership, name='cancel-membership'),

    # override email confirmation
    path('my/mails/', puraverdura_admin.mails, name='mail'),
    path('my/mails/send/', puraverdura_admin.send_email, name='mail-send'),

    # override profile (trailing forward slach is important)
    # path('my/profile/', puraverdura.profile, name='profile'),
]
