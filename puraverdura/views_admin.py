import re
from io import BytesIO

from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template, Context
from django.utils import timezone
from django.utils.translation import gettext as _
from xlsxwriter import Workbook

from juntagrico.config import Config
from juntagrico.dao.extrasubscriptiondao import ExtraSubscriptionDao
from juntagrico.dao.extrasubscriptiontypedao import ExtraSubscriptionTypeDao
from juntagrico.dao.mailtemplatedao import MailTemplateDao
from juntagrico.dao.memberdao import MemberDao
from juntagrico.dao.sharedao import ShareDao
from juntagrico.dao.subscriptiondao import SubscriptionDao
from juntagrico.dao.subscriptionsizedao import SubscriptionSizeDao
from juntagrico.entity.depot import Depot
from juntagrico.entity.jobs import ActivityArea
from juntagrico.entity.member import Member
from juntagrico.entity.share import Share
from juntagrico.mailer import FormEmails
from juntagrico.util import return_to_previous_location
from juntagrico.util.mailer import append_attachements
from juntagrico.util.management_list import get_changedate
from juntagrico.util.pdf import return_pdf_http
from juntagrico.util.subs import subscriptions_with_assignments
from juntagrico.util.views_admin import subscription_management_list
from juntagrico.util.xls import generate_excel
from juntagrico.views import get_menu_dict


@permission_required('juntagrico.can_send_mails')
def send_email(request):
    return send_email_intern(request)


@permission_required('juntagrico.is_depot_admin')
def send_email_depot(request):
    return send_email_intern(request)


@permission_required('juntagrico.is_area_admin')
def send_email_area(request):
    return send_email_intern(request)


def send_email_intern(request):
    sent = 0
    if request.method != 'POST':
        raise Http404
    emails = set()
    sender = request.POST.get('sender')
    if request.POST.get('allsubscription') == 'on':
        m_emails = MemberDao.members_for_email_with_subscription().values_list('email',
                                                                               flat=True)
        emails.update(m_emails)
    if request.POST.get('allshares') == 'on':
        emails.update(MemberDao.members_for_email_with_shares(
        ).values_list('email', flat=True))
    if request.POST.get('all') == 'on':
        emails.update(MemberDao.members_for_email(
        ).values_list('email', flat=True))
    if request.POST.get('recipients'):
        req = request.POST.get('recipients')
        split_string = re.split(' |\r\n', request.POST.get('recipients'))
        emails.update(set(split_string))
    if request.POST.get('allsingleemail'):
        emails |= set(request.POST.get('singleemail').split(' '))
    attachements = []
    append_attachements(request, attachements)


    if len(emails) > 0:
        FormEmails.internal(
            request.POST.get('subject'),
            request.POST.get('message'),
            request.POST.get('textMessage'),
            emails, attachements, sender=sender
        )
        sent = len(emails)
    return redirect('mail-result', numsent=sent)

