from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Div
from django.forms import CharField, PasswordInput, Form, ValidationError, \
    ModelForm, DateInput, IntegerField, BooleanField, HiddenInput
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from schwifty import IBAN

from juntagrico.config import Config
from juntagrico.dao.memberdao import MemberDao
from juntagrico.dao.subscriptionproductdao import SubscriptionProductDao
from juntagrico.dao.subscriptiontypedao import SubscriptionTypeDao
from juntagrico.models import Member, Subscription

class Slider(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(template='forms/slider.html', css_class='slider', *args, **kwargs)

class MemberProfileForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email',
                  'addr_street', 'addr_zipcode', 'addr_location',
                  'birthday', 'phone', 'mobile_phone', 'iban', 'reachable_by_email']
        labels = {
            "phone": _("Telefonnummer"),
            "email": _("E-Mail-Adresse"),
            "birthday": _("Geburtstag"),
            "addr_street": _("Strasse/Nr."),
            "reachable_by_email": _(
                'Sollen andere {} dich via Kontaktformular erreichen können?'
            ).format(Config.vocabulary('member_pl')),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].disabled = True
        self.fields['last_name'].disabled = True
        self.fields['email'].disabled = True
        self.fields['last_name'].help_text = self.contact_admin_link(_('Kontaktiere {} um den Namen zu ändern.'))
        self.fields['email'].help_text = self.contact_admin_link(_('Kontaktiere {} um die E-Mail-Adresse zu ändern.'))

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

        self.helper.layout = Layout(
            'first_name', 'last_name',
            'addr_street', 'addr_zipcode', 'addr_location',
            'phone', 'mobile_phone', 'email', 'birthday', 'iban',
            Slider('reachable_by_email'),
            FormActions(
                Submit('submit', _('Personalien ändern'), css_class='btn-success'),
            ),
        )

    @staticmethod
    def contact_admin_link(text):
        return mark_safe(
            escape(
                text
            ).format('<a href="mailto:{0}">{0}</a>'.format(Config.info_email()))
        )

    def clean_iban(self):
        if self.data['iban'] != '':
            try:
                IBAN(self.data['iban'])
            except ValueError:
                raise ValidationError(_('IBAN ist nicht gültig'))
        return self.data['iban']