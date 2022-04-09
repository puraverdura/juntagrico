from django.contrib.auth.decorators import login_required, permission_required
from juntagrico.dao.memberdao import MemberDao

from django.shortcuts import render

from django.utils.translation import gettext_lazy as _



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