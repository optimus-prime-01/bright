# Generated by Django 5.2.1 on 2025-05-17 17:41

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('loan_type', models.CharField(choices=[('credit_card', 'Credit Card')], max_length=20)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('term_period', models.IntegerField()),
                ('disbursement_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='active', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_user_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('aadhar_id', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('annual_income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('credit_score', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(900)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EMI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('principal_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_api.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billing_date', models.DateField()),
                ('due_date', models.DateField()),
                ('minimum_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_api.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_api.loan')),
            ],
        ),
        migrations.AddField(
            model_name='loan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_api.user'),
        ),
    ]
