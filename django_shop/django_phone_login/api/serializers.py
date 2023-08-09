import re
from rest_framework import serializers
from ...api.valiators import validate_phone_number

class PhoneTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[validate_phone_number], required=True)


class ConfirmTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[validate_phone_number], required=True)
    otp = serializers.IntegerField()
