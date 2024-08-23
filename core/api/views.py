from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.api.serializers import PaymentSerializer
from core.sdk import PaymentSDK


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_key = request.headers.get('Authorization')
        sdk = PaymentSDK(api_key=api_key)
        try:
            sdk.process_payment(**serializer.validated_data)
            return Response({"status": "Payment processed successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
