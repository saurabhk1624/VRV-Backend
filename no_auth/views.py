from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.response import CustomResponse
from no_auth.models import User
from no_auth.serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        profile = User.objects.filter(id=user).first()
        serializer = ProfileSerializer(profile)
        return CustomResponse(message=serializer.data, status=200)
