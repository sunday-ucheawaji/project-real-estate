from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profiles.models import Profile

from .models import Rating

User = get_user_model()


class CreateAgentReviewAPIView(APIView):

    def post(self, request, profile_id):
        agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
        data = request.data

        profile_user = User.objects.get(pkid=agent_profile.user.pkid)
        if profile_user.email == request.user.email:
            formatted_response = {"message": "You can't rate yourself"}
            return Response(formatted_response, status=status.HTTP_403_FORBIDDEN)

        already_exists = agent_profile.agent_review.filter(
            agent__pkid=profile_user.pkid
        ).exist()
        if already_exists:
            formatted_response = {"detail": "Profile already reviewed"}
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
        elif data["rating"] == 0:
            formatted_response = {"detail": "Profile select a rating"}
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            Rating.objects.create(
                rater=request.user,
                agent=agent_profile,
                rating=data["rating"],
                comment=data["comment"],
            )
            reviews = agent_profile.agent_review.all()
            agent_profile.num_reviews = len(reviews)

            total = 0
            for i in reviews:
                total += i.rating

            return Response("Review Added")
