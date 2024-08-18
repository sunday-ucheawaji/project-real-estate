from celery import shared_task
from django.core import mail
from real_estate.settings import development
from apps.users.models import User

@shared_task(bind=True)
def send_email(self):
    
    register_data = User.objects.values().all()

    for data in register_data: 
        mail_subject= "Learning celery"
        message = "Using celery to mail to the registered users"
        email_id = data['email']
        mail.send_mail(subject=mail_subject,message=message,from_email=development.EMAIL_HOST_USER,recipient_list=[email_id],fail_silently=False)
    
      
    return "Done sending mails"

# use this in a view function like this
# send_email.delay()