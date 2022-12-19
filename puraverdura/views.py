from django.contrib.auth.decorators import login_required, permission_required
from juntagrico.dao.memberdao import MemberDao

from django.shortcuts import render

from django.utils.translation import gettext_lazy as _

from juntagrico.forms import NonCoopMemberCancellationForm, \
    CoopMemberCancellationForm
from juntagrico.util.temporal import next_membership_end_date
from django.shortcuts import render, redirect
from puraverdura.views_subscription import cancel_subscription


#@permission_required('juntagrico.can_filter_members')
@login_required
def filters_emails(request):
    members = MemberDao.active_members()
    renderdict = {
        'members': members
    }    
    return render(request, 'members_only_emails.html', renderdict)

@login_required
def tutorials(request):
    '''
    tutorials
    '''
    return render(request, 'tutorials.html', {})


@login_required
def cancel_membership(request):
    # member = request.user.member
    # sub = member.subscription_current
    return cancel_subscription(request, subscription_id=None)

# @login_required
# def cancel_membership(request):
#     member = request.user.member
#     coop_member = member.is_cooperation_member
#     if coop_member:
#         form_type = CoopMemberCancellationForm
#     else:
#         form_type = NonCoopMemberCancellationForm
#     if request.method == 'POST':
#         form = form_type(request.POST, instance=member)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = form_type(instance=member)
#     asc = member.usable_shares_count
#     sub = member.subscription_current
#     f_sub = member.subscription_future
#     future_active = f_sub is not None and (f_sub.state == 'active' or f_sub.state == 'waiting')
#     current_active = sub is not None and (sub.state == 'active' or sub.state == 'waiting')
#     future = future_active and f_sub.share_overflow - asc < 0
#     current = current_active and sub.share_overflow - asc < 0
#     share_error = future or current
#     can_cancel = not share_error and not future_active and not current_active
#     if not can_cancel:
#         return cancel_subscription(request, subscription_id=sub.id)
#     renderdict = {
#         'coop_member': coop_member,
#         'end_date': next_membership_end_date(),
#         'member': member,
#         'can_cancel': can_cancel,
#         'share_error': share_error,
#         'form': form
#     }
#     return render(request, 'cancelmembership.html', renderdict)

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