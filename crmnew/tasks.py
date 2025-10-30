from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_lead_converted_email(lead_name, user_email, deal_title=None):
    
    subject = f" Lead '{lead_name}' has been successfully converted!"
    
    message = (
        f"Hello,\n\n"
        f"The lead '{lead_name}' has just been converted into a deal"
        + (f" titled '{deal_title}'." if deal_title else ".") +
        "\n\nPlease check the CRM dashboard for more details."
        "\n\nThank you,\nCRM System"

    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"✅ Email notification sent to {user_email} for converted lead '{lead_name}'")

@shared_task
def send_assigned_email(object_name, item_name, user_email):
    subject = f"New {object_name} Assigned to you"
    message = (
        f"Hi, you have been assigned a new  {object_name.lower()}: {item_name}. "
        f"Please check your dashboard for details."
        "\n\nThank you,\nCRM System"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"✅ Assignment email sent to {user_email} for {object_name}")
