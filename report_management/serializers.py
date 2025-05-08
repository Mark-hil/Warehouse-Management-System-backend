from rest_framework import serializers
from .models import ReportItem, MaintenanceHistory

class ReportItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportItem
        fields = '__all__'

class MaintenanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceHistory
        fields = '__all__'
