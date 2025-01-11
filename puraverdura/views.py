from django.contrib.auth.decorators import login_required, permission_required
from juntagrico.dao.memberdao import MemberDao
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from puraverdura.views_subscription import cancel_subscription

@login_required
def filters_emails(request):
    members = MemberDao.active_members()
    renderdict = {
        'members': members
    }
    return render(request, 'members_only_emails.html', renderdict)

@login_required
def tutorials(request):
    return render(request, 'tutorials.html', {})

@login_required
def cancel_membership(request):
    return cancel_subscription(request, subscription_id=None)

