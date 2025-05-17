from celery import shared_task
import pandas as pd
from .models import User

@shared_task
def calculate_credit_score(user_id):
    user = User.objects.get(id=user_id)
    df = pd.read_csv('credit_data.csv')
    user_data = df[df['aadhar_id'] == user.aadhar_id]
    balance = user_data['CREDIT'].sum() - user_data['DEBIT'].sum()
    
    if balance >= 1000000:
        credit_score = 900
    elif balance <= 10000:
        credit_score = 300
    else:
        credit_score = 300 + (balance - 10000) * (600) / (990000)
        credit_score = min(900, max(300, int(credit_score)))
    
    user.credit_score = credit_score
    user.save()
    return credit_score

@shared_task
def process_daily_billing():
    from datetime import date, timedelta
    from .models import Loan, Bill
    
    today = date.today()
    loans = Loan.objects.filter(status='active')
    
    for loan in loans:
        last_bill = Bill.objects.filter(loan=loan).order_by('-billing_date').first()
        
        if not last_bill or (today - last_bill.billing_date).days >= 30:
            principal_balance = loan.loan_amount
            min_due = (principal_balance * 0.03)
            
            Bill.objects.create(
                loan=loan,
                billing_date=today,
                due_date=today + timedelta(days=15),
                minimum_due=min_due,
                total_due=principal_balance
            )