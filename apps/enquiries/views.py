from django.core.mail import send_mail
from real_estate.settings.development import DEFAULT_FROM_EMAIL
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Enquiry


class SendEnquiryEmailAPIView(APIView):

    def post(self, request):
        data = request.data

        try:
            subject = data["subject"]
            name = data["name"]
            email = data["email"]
            message = data["message"]
            from_email = data["email"]
            recipient_list = data[DEFAULT_FROM_EMAIL]

            send_mail(subject, message, from_email, recipient_list,
                    fail_silently=True)

            enquiry = Enquiry(name=name, email=email,
                               subject=subject, message=message)
            enquiry.save()

            return Response({"success": "Your enquiry was successfully submitted"})
        except:
            return Response({"fail": "Enquiry was not sent. Please try again."})

