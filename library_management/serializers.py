from rest_framework import serializers


class APIRootResponseSerializer(serializers.Serializer):
    """Serializer for API root response"""
    message = serializers.CharField()
    endpoints = serializers.DictField()
    admin = serializers.CharField()
    documentation = serializers.DictField()
