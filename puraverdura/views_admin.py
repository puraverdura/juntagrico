import re

from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.utils import timezone

from juntagrico.dao.memberdao import MemberDao
from juntagrico.mailer import append_attachements
from juntagrico.mailer import formemails, EmailSender
from juntagrico.view_decorators import any_permission_required

from django.conf import settings


@permission_required('juntagrico.can_send_mails')
def send_email(request):
    return send_email_intern(request)


@permission_required('juntagrico.is_depot_admin')
def send_email_depot(request):
    return send_email_intern(request)


@permission_required('juntagrico.is_area_admin')
def send_email_area(request):
    return send_email_intern(request)


@any_permission_required('juntagrico.is_area_admin', 'juntagrico.can_send_mails')
def send_email_job(request):
    return send_email_intern(request)


def send_email_intern(request, max_num_emails=50):
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
        emails.update(re.split(r'[\s,;]+', request.POST.get('recipients')))
    if request.POST.get('allsingleemail'):
        emails.update(re.split(r'[\s,;]+', request.POST.get('singleemail')))

    files = []
    append_attachements(request, files)

    num_emails = len(emails)

    if num_emails > 0:
        emails_subsets = [list(emails)[i:i + max_num_emails] for i in range(0, num_emails, max_num_emails)]
        timestamps = []
        for em in emails_subsets:
            timestamps.append(timezone.now())
            formemails.internal(
                request.POST.get('subject'),
                request.POST.get('message'),
                request.POST.get('textMessage'),
                set(em), files, sender=sender
            )
            #print(f'Emails: {em}')
            #print(f'sender: {sender}')
        sent = num_emails
        # Send Debug Email
        admin_email = getattr(settings, 'DEBUG_MAILER_ADMIN', None)
        if admin_email is not None:
            admin_message = ''
            for em_list, t in zip(emails_subsets, timestamps):
                admin_message = admin_message + str(t) + ': ' + str(em_list) + ',\n'
            
            print(admin_email)
            print(admin_message)
            EmailSender.get_sender('[JUNTAGRICO] sent emails', admin_message, bcc=[admin_email], from_email=sender).send()

    return redirect('mail-result', numsent=sent)