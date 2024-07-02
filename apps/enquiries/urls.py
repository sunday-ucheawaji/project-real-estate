from django.urls import path
from . import views



urlpatterns = [
    path("", views.SendEnquiryEmailAPIView.as_view(), name="send-enquiry") 
]