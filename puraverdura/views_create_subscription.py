from django.shortcuts import render, redirect
from juntagrico.forms import SubscriptionForm
from juntagrico.util import temporal
from juntagrico.view_decorators import create_subscription_session


# This function overrides
# https://github.com/juntagrico/juntagrico/blob/f32d36b24e159658cf6353c4497ae286eb318fb3/juntagrico/views_create_subscription.py#L51
@create_subscription_session
def cs_select_start_date(request, cs_session):
    subscription_form = SubscriptionForm(initial={
        'start_date': cs_session.start_date or temporal.start_of_next_business_year()
    })
    if request.method == 'POST':
        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():
            cs_session.start_date = subscription_form.cleaned_data['start_date']
            return redirect(cs_session.next_page())
    render_dict = {
        'start_date': temporal.start_of_next_business_year(),
        'start_date_current_year': temporal.start_of_business_year(),
        'subscriptionform': subscription_form,
    }
    return render(request, 'createsubscription/select_start_date.html', render_dict)
