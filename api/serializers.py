from rest_framework import serializers
from .models import (
    User, IncomeCategory, Income, ExpenseCategory, Expense,
    SavingsGoal, PerformanceMetric, Subscription, Payment
)
from django.contrib.auth.hashers import make_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'iso2Country', 'iso3Country',
            'address', 'email', 'date_of_birth', 'birth_date', 'status',
            'phone', 'active', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    category = IncomeCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Income
        fields = ['id', 'name', 'description', 'date', 'price', 'category', 'category_id']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Expense
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = '__all__'

class SavingsGoalSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    income_categories = IncomeCategorySerializer(many=True, read_only=True)
    expense_categories = ExpenseCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGoal
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date', 
            'total_target_amount', 'currency', 'saving_history', 
            'priority', 'user', 'user_id', 'income_categories', 
            'expense_categories', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
