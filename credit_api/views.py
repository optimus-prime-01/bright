from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from datetime import date, timedelta
from decimal import Decimal
from .models import User, Loan, EMI, Payment
from .serializers import (UserSerializer, LoanSerializer, EMISerializer,
                         PaymentSerializer, StatementSerializer)
from .tasks import calculate_credit_score

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calculate_credit_score.delay(user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def apply_loan(request):
    try:
        user = User.objects.get(unique_user_id=request.data['unique_user_id'])
        if user.credit_score < 450:
            return Response({"error": "Credit score too low"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        if user.annual_income < 150000:
            return Response({"error": "Annual income too low"}, 
                          status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, 
                      status=status.HTTP_404_NOT_FOUND)

    loan_amount = Decimal(request.data['loan_amount'])
    if loan_amount > 5000:
        return Response({"error": "Loan amount too high"}, 
                      status=status.HTTP_400_BAD_REQUEST)

    interest_rate = Decimal(request.data['interest_rate'])
    term_period = int(request.data['term_period'])
    
    if interest_rate < 12:
        return Response({"error": "Interest rate too low"}, 
                      status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        loan_data = {
            'user': user.id,
            'loan_type': request.data['loan_type'],
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'term_period': term_period,
            'disbursement_date': request.data['disbursement_date']
        }
        
        loan_serializer = LoanSerializer(data=loan_data)
        if loan_serializer.is_valid():
            loan = loan_serializer.save()
            emi_schedule = calculate_emi_schedule(loan)
            EMI.objects.bulk_create(emi_schedule)
            
            return Response({
                "loan_id": loan.loan_id,
                "emi_schedule": EMISerializer(emi_schedule, many=True).data
            })
        return Response(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def make_payment(request):
    try:
        loan = Loan.objects.get(loan_id=request.data['loan_id'])
        amount = Decimal(request.data['amount'])
        
        if Payment.objects.filter(loan=loan, 
                                payment_date=date.today()).exists():
            return Response({"error": "Payment already made today"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if EMI.objects.filter(loan=loan, 
                            due_date__lt=date.today(),
                            status='pending').exists():
            return Response({"error": "Previous EMI not paid"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            payment = Payment.objects.create(loan=loan, amount=amount)
            
            current_emi = EMI.objects.filter(loan=loan, 
                                           status='pending').order_by('due_date').first()
            if current_emi:
                if amount >= current_emi.total_amount:
                    current_emi.status = 'paid'
                    current_emi.paid_amount = current_emi.total_amount
                    current_emi.payment_date = date.today()
                else:
                    current_emi.paid_amount = amount
                current_emi.save()
            
            return Response({"message": "Payment successful"})
            
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, 
                      status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_statement(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
        past_transactions = EMI.objects.filter(loan=loan, 
                                             due_date__lt=date.today())
        upcoming_transactions = EMI.objects.filter(loan=loan, 
                                                 due_date__gte=date.today())
        
        data = {
            'past_transactions': past_transactions,
            'upcoming_transactions': upcoming_transactions
        }
        
        serializer = StatementSerializer(data)
        return Response(serializer.data)
        
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, 
                      status=status.HTTP_404_NOT_FOUND)

def calculate_emi_schedule(loan):
    emi_schedule = []
    principal = loan.loan_amount
    rate = loan.interest_rate / (12 * 100)
    term = loan.term_period
    
    emi = principal * rate * (1 + rate)**term / ((1 + rate)**term - 1)
    
    current_date = loan.disbursement_date
    
    for _ in range(term):
        interest = principal * rate
        principal_part = emi - interest
        
        current_date += timedelta(days=30)
        
        emi_schedule.append(EMI(
            loan=loan,
            due_date=current_date,
            principal_amount=principal_part,
            interest_amount=interest,
            total_amount=emi
        ))
        
        principal -= principal_part
    
    return emi_schedule
