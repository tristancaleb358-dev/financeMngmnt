from django.shortcuts import render
from rest_framework import permissions, viewsets
from .serializers import CustomerSerializer
from .models import CUSTOMER


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = CUSTOMER.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
