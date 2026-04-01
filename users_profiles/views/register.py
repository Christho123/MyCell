from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.register import PublicRegisterSerializer


class PublicRegisterView(APIView):
    """
    Registro público (sin JWT ni sesión). Pensado para el flujo del frontend.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PublicRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Usuario registrado con éxito"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
