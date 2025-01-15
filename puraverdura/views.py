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


def create_members_csv_content(members):
    content = "first_name,last_name,email\n"
    for member in members:
        member_info = member.first_name + ',' + member.last_name + "," + member.email
        content += member_info + '\n'

    return content

@permission_required('juntagrico.can_view_exports')
def csv_export_members_sub(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="Mitglieder_mit_Ernteanteilen.csv"'},
    )
    members_with_sub = MemberDao.members_for_email_with_subscription()

    content = create_members_csv_content(members_with_sub)
    response.write(content)
    return response


@permission_required('juntagrico.can_view_exports')
def csv_export_members_shares(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="Mitglieder_mit_Anteilsscheinen.csv"'},
    )
    MemberDao.members_for_email_with_subscription()
    members_with_shares = MemberDao.members_for_email_with_shares()

    content = create_members_csv_content(members_with_shares)
    response.write(content)
    return response

@permission_required('juntagrico.can_view_exports')
def csv_export_all_members(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="Alle_Mitglieder.csv"'},
    )
    MemberDao.all_members()
    members = MemberDao.members_for_email()

    content = create_members_csv_content(members)
    response.write(content)
    return response
