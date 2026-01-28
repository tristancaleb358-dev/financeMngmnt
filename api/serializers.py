from rest_framework import serializers
from .models import CUSTOMER

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CUSTOMER
        fields = ['first_name', 'last_name', 'address', 'email', 'mobile', 'password', 'date_of_birth', 'abonnement_type', 'status', 'customer_type', 'created_at',
         'updated_at', 'updated_by', 'created_by']