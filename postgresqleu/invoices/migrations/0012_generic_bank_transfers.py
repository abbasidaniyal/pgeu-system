# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-09 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
        ('invoices', '0011_drop_auto_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransferFees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PendingBankMatcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pattern', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('foraccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Account')),
                ('journalentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.JournalEntry')),
            ],
        ),
        migrations.CreateModel(
            name='PendingBankTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('methodidentifier', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transtext', models.CharField(blank=True, max_length=500)),
                ('sender', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True, max_length=2000)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.InvoicePaymentMethod')),
            ],
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='bankinfo',
        ),
        migrations.AddField(
            model_name='banktransferfees',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Invoice'),
        ),
    ]
