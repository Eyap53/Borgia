# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-31 19:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=255)),
                ('account', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_bank_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_bankaccount', 'Afficher un compte en banque'), ('list_bankaccount', 'Lister les comptes en banque')),
            },
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_cash', 'Afficher des espèces'), ('list_cash', 'Lister les espèces')),
            },
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('is_cashed', models.BooleanField(default=False)),
                ('signature_date', models.DateField(default=django.utils.timezone.now)),
                ('cheque_number', models.CharField(max_length=7)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheque_bank_account', to='finances.BankAccount')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheque_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheque_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_cheque', 'Afficher un cheque'), ('list_cheque', 'Lister les chèques')),
            },
        ),
        migrations.CreateModel(
            name='DebitBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_debit_balance', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_debit_balance', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_debitbalance', 'Afficher un débit sur compte foyer'), ('list_debitbalance', 'Lister les débits sur comptes foyers')),
            },
        ),
        migrations.CreateModel(
            name='Lydia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_operation', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('id_from_lydia', models.CharField(max_length=255)),
                ('banked', models.BooleanField(default=False)),
                ('date_banked', models.DateField(blank=True, null=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lydia_recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lydia_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_lydia', 'Afficher un virement Lydia'), ('list_lydia', 'Lister les virements Lydias')),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('cashs', models.ManyToManyField(blank=True, to='finances.Cash')),
                ('cheques', models.ManyToManyField(blank=True, to='finances.Cheque')),
                ('debit_balance', models.ManyToManyField(blank=True, to='finances.DebitBalance')),
                ('lydias', models.ManyToManyField(blank=True, to='finances.Lydia')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator_sale', to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finances.Payment')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_sale', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_sale', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('retrieve_sale', 'Afficher une vente'), ('list_sale', 'Lister les ventes'), ('add_transfert', "Effectuer un transfert d'argent")),
            },
        ),
        migrations.CreateModel(
            name='SharedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=254)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('bills', models.CharField(blank=True, max_length=254, null=True)),
                ('done', models.BooleanField(default=False)),
                ('ponderation', models.CharField(default='[]', max_length=10000)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, related_name='participants', to=settings.AUTH_USER_MODEL)),
                ('registered', models.ManyToManyField(blank=True, related_name='registered', to=settings.AUTH_USER_MODEL)),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finances.Sale')),
            ],
            options={
                'permissions': (('register_sharedevent', "S'inscrire à un événement commun"), ('list_sharedevent', 'Lister les événements communs'), ('manage_sharedevent', 'Gérer les événements communs'), ('proceed_payment_sharedevent', 'Procéder au paiement des événements communs')),
            },
        ),
    ]
