from django.shortcuts import render
from rest_framework import permissions, viewsets
from .serializers import CustomerSerializer
from .models import User

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    User, IncomeCategory, Income, ExpenseCategory, Expense,
    SavingsGoal, PerformanceMetric, Subscription, Payment
)
from .serializers import (
    CustomerSerializer, IncomeCategorySerializer, IncomeSerializer,
    ExpenseCategorySerializer, ExpenseSerializer, SavingsGoalSerializer,
    PerformanceMetricSerializer, SubscriptionSerializer, PaymentSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée : l'utilisateur peut modifier uniquement ses propres données
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user if hasattr(obj, 'user') else True


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('created_at')
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['active', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'updated_at']

    def get_permissions(self):
        """
        Permissions instantanées : lecture pour tous, modification pour propriétaire
        """
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class IncomeCategoryViewSet(viewsets.ModelViewSet):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__name']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category__name']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class SavingsGoalViewSet(viewsets.ModelViewSet):
    queryset = SavingsGoal.objects.all().order_by('created_at')
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['priority', 'currency', "user", "user__first_name", "user__last_name", "user__phone"]
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'total_target_amount']

    

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Calculer l'avancement de l'objectif d'épargne"""
        goal = self.get_object()
        total_saved = sum(item.get('amount', 0) for item in goal.saving_history)
        progress = (total_saved / goal.total_target_amount) * 100
        return Response({'progress': progress, 'total_saved': total_saved})


class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def get_queryset(self):
    #     return self.queryset.filter(goal__user=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['currency']
    search_fields = ['subscription__name']
    ordering_fields = ['period']

    # def get_queryset(self):
    #     return self.queryset.filter(subscription__user=self.request.user)