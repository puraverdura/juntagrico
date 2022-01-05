from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from juntagrico.config import Config
from juntagrico.util.pdf import render_to_pdf_http


@login_required
def share_certificate(request):
    year = int(request.GET['year'])
    member = request.user.member
    active_share_years = member.active_share_years
    if year >= timezone.now().year or year not in active_share_years:
        return error_page(request, _('{}-Bescheinigungen können nur für vergangene Jahre ausgestellt werden.').format(Config.vocabulary('share')))
    shares_date = date(year, 12, 31)
    shares = member.active_shares_for_date(date=shares_date).values('value').annotate(count=Count('value')).annotate(total=Sum('value')).order_by('value')
    
    share_id = [str(id['id']) for id in member.active_shares_for_date(date=shares_date).values('id')]
    share_id_str = ', '.join(share_id)
    
    shares_total = 0
    for share in shares:
        shares_total = shares_total + share['total']
    renderdict = {
        'member': member,
        'cert_date': timezone.now().date(),
        'shares_date': shares_date,
        'shares': shares,
        'shares_total': shares_total,
        'share_ids':share_id_str
    }
    return render_to_pdf_http('exports/share_certificate.html', renderdict, _('Bescheinigung') + str(year) + '.pdf')


def error_page(request, error_message):
    renderdict = {'error_message': error_message}
    return render(request, 'error.html', renderdict)