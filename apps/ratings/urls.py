from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:profile_id>/",
        views.CreateAgentReviewAPIView.as_view(),
        name="create-rating",
    ),
]
