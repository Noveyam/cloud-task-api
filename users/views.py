from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        return Response(
            {
                'id': str(user.id),
                'email': user.email,
                'full_name': user.full_name,
            },
            status=status.HTTP_201_CREATED,
        )