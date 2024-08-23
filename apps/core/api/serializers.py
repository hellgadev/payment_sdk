from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['credit_card', 'paypal', 'crypto'])
    amount = serializers.FloatField()
    currency = serializers.ChoiceField(
        choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('BTC', 'Bitcoin')],
        allow_blank=True
    )
