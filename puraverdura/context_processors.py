from django.conf import settings


def staging(request):
    return {'IS_STAGING': settings.IS_STAGING}
