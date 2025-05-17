from rest_framework import serializers
from .models import User, Loan, EMI, Payment, Bill

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['unique_user_id', 'aadhar_id', 'name', 'annual_income', 'credit_score']
        read_only_fields = ['unique_user_id', 'credit_score']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_id', 'user', 'loan_type', 'loan_amount', 'interest_rate', 
                 'term_period', 'disbursement_date']
        read_only_fields = ['loan_id']

class EMISerializer(serializers.ModelSerializer):
    class Meta:
        model = EMI
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['loan', 'amount', 'payment_date']

class StatementSerializer(serializers.Serializer):
    past_transactions = EMISerializer(many=True)
    upcoming_transactions = EMISerializer(many=True)