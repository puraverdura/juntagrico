from datetime import date

import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext as _
from django.conf import settings
from django import forms

from juntagrico.entity.subs import Subscription
from juntagrico.config import Config
from juntagrico.util.pdf import render_to_pdf_http
from juntagrico.util.temporal import end_of_next_business_year, end_of_business_year, \
    cancelation_date, next_membership_end_date
from juntagrico.util.management import cancel_sub, cancel_share
from juntagrico.view_decorators import primary_member_of_subscription
from juntagrico.mailer import adminnotification

from schwifty import IBAN


@login_required
def share_certificate(request):
    year = int(request.GET['year'])
    member = request.user.member
    active_share_years = member.active_share_years
    if year >= timezone.now().year or year not in active_share_years:
        return error_page(request, _('{}-Bescheinigungen können nur für vergangene Jahre ausgestellt werden.').format(
            Config.vocabulary('share')))
    shares_date = date(year, 12, 31)
    shares = member.active_shares_for_date(date=shares_date).values('value').annotate(count=Count('value')).annotate(
        total=Sum('value')).order_by('value')

    share_id = [str(id['number']) for id in
                member.active_shares_for_date(date=shares_date).values('number').order_by('number')]
    share_id_str = ', '.join(share_id)

    logo_url = os.path.join(settings.STATIC_ROOT, 'img', 'Pura-Verdura-logo.png')
    # print(logo_url)
    # print(share_id_str)
    # share_set = member.active_shares_for_date(date=shares_date)
    # print(share_set[0].__dict__)

    shares_total = 0
    for share in shares:
        shares_total = shares_total + share['total']
    renderdict = {
        'member': member,
        'cert_date': timezone.now().date(),
        'shares_date': shares_date,
        'shares': shares,
        'shares_total': shares_total,
        'share_ids': share_id_str,
        'logo_url': logo_url
    }
    return render_to_pdf_http('exports/share_certificate.html', renderdict, _('Bescheinigung') + str(year) + '.pdf')


def error_page(request, error_message):
    renderdict = {'error_message': error_message}
    return render(request, 'error.html', renderdict)


class MembershipAndSubscriptionCancellationForm(forms.Form):
    regular_or_now_choices = [('regular', 'regulär'),
                              ('now', 'ab jetzt')]
    regular_or_now = forms.ChoiceField(choices=regular_or_now_choices, widget=forms.RadioSelect, initial='regular')

    cancel_membership_choices = [('no', 'Ich möchte Mitglied bei Pura Verdura bleiben'),
                                 ('yes', 'Ich möchte meine Mitgliedschaft auch kündigen')]
    cancel_membership = forms.ChoiceField(choices=cancel_membership_choices, widget=forms.RadioSelect, initial='no')

    iban = forms.CharField(label='iban', required=False)
    message = forms.CharField(label='message', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        if 'juntagrico_member' in kwargs:
            member = kwargs.pop('juntagrico_member')
        else:
            member = None
        super(MembershipAndSubscriptionCancellationForm, self).__init__(*args, **kwargs)
        if member:
            self.fields['iban'].initial = member.iban

    def clean_iban(self):
        iban = self.data.get('iban', '')
        if not iban:
            return
        try:
            IBAN(iban)
        except ValueError:
            raise forms.ValidationError(_('IBAN ist nicht gültig'))
        return iban


# @primary_member_of_subscription
def cancel_subscription(request, subscription_id):
    # Subscription
    # subscription = get_object_or_404(Subscription, id=subscription_id)

    if request.user.is_authenticated:
        member = request.user.member
    else:
        return redirect('login')

    now = timezone.now().date()
    end_date_sub = end_of_business_year() if now <= cancelation_date() else end_of_next_business_year()
    # Membership and Subscription
    asc = member.usable_shares_count
    sub = member.subscription_current
    f_sub = member.subscription_future

    future_active = f_sub is not None and (f_sub.state == 'active' or f_sub.state == 'waiting')
    current_active = sub is not None and (sub.state == 'active' or sub.state == 'waiting')
    future = future_active and f_sub.share_overflow - asc < 0
    current = current_active and sub.share_overflow - asc < 0
    share_error = future or current
    can_cancel = not share_error and not future_active and not current_active

    # end_date_mem = next_membership_end_date()
    end_date_mem = end_date_sub

    if request.method == 'POST':
        form = MembershipAndSubscriptionCancellationForm(request.POST, juntagrico_member=member)
        if form.is_valid():
            iban = form.cleaned_data['iban']
            if iban:
                member.iban = iban
                member.save()
            regular_or_now = form.cleaned_data['regular_or_now']
            if regular_or_now == 'now':
                end_date_sub = now
                end_date_mem = now
            cancel_membership = form.cleaned_data['cancel_membership']
            message = form.cleaned_data['message']
            admin_message = \
                f"""
                Mitglied: {member.first_name} {member.last_name}\n\n
                Email: {member.email}\n\n
                Gewünschter Kündigungszeitpunkt: {regular_or_now}\n\n
                Soll Mitgliedschaft gekündigt werden: {cancel_membership}\n\n
                IBAN: {iban}\n\n
                Nachricht:\n
                {message}
                """
            print(admin_message)
            adminnotification.subscription_canceled(sub, admin_message)
            if current_active and sub.primary_member.id == member.id:
                cancel_sub(sub, end_date_sub, admin_message)
            if cancel_membership == 'yes':
                member.end_date = end_date_mem
                member.cancellation_date = now
                [cancel_share(s, now, end_date_mem) for s in member.active_shares]
                member.save()
                return redirect('profile')

            return redirect('sub-detail')
    else:
        form = MembershipAndSubscriptionCancellationForm(juntagrico_member=member)
    renderdict = {
        'end_date_sub': end_date_sub,
        'end_date_mem': end_date_mem,
        'form': form,
    }
    return render(request, 'cancelsubscription.html', renderdict)
