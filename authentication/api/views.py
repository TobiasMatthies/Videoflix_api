from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . serializers import RegistrationSerializer

# Create your views here.
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
