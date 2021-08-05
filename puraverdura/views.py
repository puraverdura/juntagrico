# import vobject

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from juntagrico.dao.memberdao import MemberDao
from juntagrico.dao.subscriptiondao import SubscriptionDao
from juntagrico.dao.subscriptionproductdao import SubscriptionProductDao
from juntagrico.dao.subscriptiontypedao import SubscriptionTypeDao
from juntagrico.entity.jobs import ActivityArea
from openpyxl import Workbook

import base64
import hmac
import hashlib
from urllib import parse
from django.conf import settings


from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from juntagrico.models import Member, Subscription

from juntagrico.dao.depotdao import DepotDao
from juntagrico.dao.listmessagedao import ListMessageDao
from juntagrico.dao.subscriptionsizedao import SubscriptionSizeDao
from juntagrico.util.pdf import render_to_pdf_http
from juntagrico.util.temporal import weekdays, start_of_business_year, end_of_business_year
from juntagrico.config import Config
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from openpyxl.utils import get_column_letter

from puraverdura.utils.stats import assignments_by_subscription, assignments_by_day, slots_by_day, \
    members_with_assignments, members_with_assignments_no_filter
from puraverdura.utils.utils import date_from_get, get_delivery_dates_of_month

from puraverdura.forms import MemberProfileForm



#@permission_required('juntagrico.can_filter_members')
def filters_emails(request):
    members = MemberDao.active_members()

    renderdict = get_menu_dict(request)
    renderdict.update({
        'members': members
    })
    
    return render(request, 'members_only_emails.html', renderdict)

# tutorial webpage
@login_required
def tutorials(request):
    renderdict = get_menu_dict(request)
    return render(request, 'tutorials.html', renderdict)


# @login_required
# def profile(request):
#     success = False
#     member = request.user.member
#     if request.method == 'POST':
#         memberform = MemberProfileForm(request.POST, instance=member)
#         if memberform.is_valid():
#             # set all fields of user
#             member.first_name = memberform.cleaned_data['first_name']
#             member.last_name = memberform.cleaned_data['last_name']
#             member.email = memberform.cleaned_data['email']
#             member.addr_street = memberform.cleaned_data['addr_street']
#             member.addr_zipcode = memberform.cleaned_data['addr_zipcode']
#             member.addr_location = memberform.cleaned_data['addr_location']
#             member.phone = memberform.cleaned_data['phone']
#             member.mobile_phone = memberform.cleaned_data['mobile_phone']
#             member.iban = memberform.cleaned_data['iban']
#             member.reachable_by_email = memberform.cleaned_data['reachable_by_email']
#             member.save()
#             success = True
#     else:
#         memberform = MemberProfileForm(instance=member)
#     renderdict = get_menu_dict(request)
#     renderdict.update({
#         'memberform': memberform,
#         'success': success,
#         'member': member,
#         'menu': {'personalInfo': 'active'},
#     })
#     return render(request, 'profile.html', renderdict)