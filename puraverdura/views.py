from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from juntagrico.dao.memberdao import MemberDao
from django.shortcuts import render
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


@permission_required('juntagrico.can_view_exports')
def csv_export_members_sub(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="members_with_subs.csv"'},
    )
    mebers_with_sub = MemberDao.members_for_email_with_subscription()
    content = "first_name, last_name, email \n"

    for member in mebers_with_sub:
        member_info = member.first_name + ',' + member.last_name + "," + member.email
        content += member_info + '\n'

    response.write(content)
    return response


@permission_required('juntagrico.can_view_exports')
def csv_export_members_shares(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="members_with_shares.csv"'},
    )
    MemberDao.members_for_email_with_subscription()
    mebers_with_shares = MemberDao.members_for_email_with_shares()
    content = "first_name, last_name, email \n"

    for member in mebers_with_shares:
        member_info = member.first_name + ',' + member.last_name + "," + member.email
        content += member_info + '\n'

    response.write(content)
    return response

@permission_required('juntagrico.can_view_exports')
def csv_export_all_members(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="members.csv"'},
    )
    MemberDao.all_members()
    mebers = MemberDao.members_for_email()
    content = "first_name, last_name, email \n"

    for member in mebers:
        member_info = member.first_name + ',' + member.last_name + "," + member.email
        content += member_info + '\n'

    response.write(content)
    return response
