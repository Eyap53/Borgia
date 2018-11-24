import datetime
import decimal

from django.test import TestCase

from finances.models import SharedEvent
from users.models import User

# class LydiaTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#         )
#         self.user2 = User.objects.create(
#             username='user2'
#         )
#         self.lydia = Lydia.objects.create(
#             amount=10,
#             id_from_lydia='abcdefg',
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.payment = Payment.objects.create()
#         self.payment.lydias.add(self.lydia)
#         self.payment.maj_amount()
#         self.sale = Sale.objects.create(
#             wording='',
#             sender=self.user1,
#             recipient=self.user2,
#             operator=self.user1,
#             payment=self.payment
#         )
#         self.sale.maj_amount()
#
#     def test_str(self):
#         self.assertEqual(
#             self.lydia.__str__(),
#             'Last name 1 First name 1 10€')
#
#     def test_list_transaction(self):
#         self.assertCountEqual(
#             self.lydia.list_transaction(),
#             [self.sale]
#         )
#
#
# class CashTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#         )
#         self.user2 = User.objects.create(
#             username='user2'
#         )
#         self.cash = Cash.objects.create(
#             amount=10,
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.payment = Payment.objects.create()
#         self.payment.cashs.add(self.cash)
#         self.payment.maj_amount()
#         self.sale = Sale.objects.create(
#             wording='',
#             sender=self.user1,
#             recipient=self.user2,
#             operator=self.user1,
#             payment=self.payment
#         )
#         self.sale.maj_amount()
#
#     def test_str(self):
#         self.assertEqual(
#             self.cash.__str__(),
#             'Last name 1 First name 1 10€')
#
#     def test_list_sale(self):
#         self.assertCountEqual(
#             self.cash.list_sale(),
#             [self.sale]
#         )
#
#     def test_list_payment(self):
#         self.assertCountEqual(
#             self.cash.list_payment(),
#             [self.payment]
#         )
#
#
# class ChequeTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#         )
#         self.user2 = User.objects.create(
#             username='user2'
#         )
#         self.cheque = Cheque.objects.create(
#             amount=10,
#             cheque_number='1234567',
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.payment = Payment.objects.create()
#         self.payment.cheques.add(self.cheque)
#         self.payment.maj_amount()
#         self.sale = Sale.objects.create(
#             wording='',
#             sender=self.user1,
#             recipient=self.user2,
#             operator=self.user1,
#             payment=self.payment
#         )
#         self.sale.maj_amount()
#
#     def test_str(self):
#         self.assertEqual(
#             self.cheque.__str__(),
#             'Last name 1 First name 1 10€ n°1234567')
#
#     def test_list_sale(self):
#         self.assertCountEqual(
#             self.cheque.list_sale(),
#             [self.sale]
#         )
#
#     def test_list_payments(self):
#         self.assertCountEqual(
#             self.cheque.list_payments(),
#             [self.payment]
#         )
#
#
# class DebitBalanceTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#         )
#         self.user2 = User.objects.create(
#             username='user2'
#         )
#         self.debit_balance = DebitBalance.objects.create(
#             amount=10,
#             date=datetime.date.today(),
#             sender=self.user1,
#             recipient=self.user2
#         )
#
#     def test_str(self):
#         self.assertEqual(
#             self.debit_balance.__str__(),
#             '10€ ' + str(datetime.date.today()))
#
#     def test_set_movement(self):
#         self.user1.balance = 100
#         self.user1.save()
#         self.debit_balance.set_movement()
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(90)
#         )
#         self.assertAlmostEqual(
#             self.user2.balance,
#             decimal.Decimal(0)
#         )
#
#
# class PaymentTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#         )
#         self.user2 = User.objects.create(
#             username='user2'
#         )
#         self.cheque = Cheque.objects.create(
#             amount=10,
#             cheque_number='1234567',
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.debit_balance = DebitBalance.objects.create(
#             amount=10,
#             date=datetime.date.today(),
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.cash = Cash.objects.create(
#             amount=10,
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.lydia = Lydia.objects.create(
#             amount=10,
#             id_from_lydia='abcdefg',
#             sender=self.user1,
#             recipient=self.user2
#         )
#         self.payment = Payment.objects.create()
#         self.payment.cheques.add(self.cheque)
#         self.payment.debit_balance.add(self.debit_balance)
#         self.payment.cashs.add(self.cash)
#         self.payment.lydias.add(self.lydia)
#
#     def test_str(self):
#         self.assertEqual(
#             self.payment.__str__(),
#             'payement n°' + str(self.payment.pk)
#         )
#
#     def test_list_cheque(self):
#         self.assertCountEqual(
#             self.payment.list_cheque()[0],
#             [self.cheque]
#         )
#         self.assertAlmostEqual(
#             self.payment.list_cheque()[1],
#             decimal.Decimal(10)
#         )
#
#     def test_list_lydia(self):
#         self.assertCountEqual(
#             self.payment.list_lydia()[0],
#             [self.lydia]
#         )
#         self.assertAlmostEqual(
#             self.payment.list_lydia()[1],
#             decimal.Decimal(10)
#         )
#
#     def test_list_cash(self):
#         self.assertCountEqual(
#             self.payment.list_cash()[0],
#             [self.cash]
#         )
#         self.assertAlmostEqual(
#             self.payment.list_cash()[1],
#             decimal.Decimal(10)
#         )
#
#     def test_list_debit_balance(self):
#         self.assertCountEqual(
#             self.payment.list_debit_balance()[0],
#             [self.debit_balance]
#         )
#         self.assertAlmostEqual(
#             self.payment.list_debit_balance()[1],
#             decimal.Decimal(10)
#         )
#
#     def test_maj_amount(self):
#         self.assertAlmostEqual(
#             self.payment.amount,
#             decimal.Decimal(0)
#         )
#         self.payment.maj_amount()
#         self.assertAlmostEqual(
#             self.payment.amount,
#             decimal.Decimal(40)
#         )
#
#     def test_payments_used(self):
#         self.assertCountEqual(
#             self.payment.payments_used(),
#             ['Cheque', 'Espèces', 'Lydia', 'Compte foyer']
#         )
#         payment2 = Payment.objects.create()
#         self.assertCountEqual(
#             payment2.payments_used(),
#             []
#         )
#         payment2.cashs.add(self.cash)
#         self.assertCountEqual(
#             payment2.payments_used(),
#             ['Espèces']
#         )
#         payment2.cashs.remove(self.cash)
#         self.assertCountEqual(
#             payment2.payments_used(),
#             []
#         )
#
#
# class SaleTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             last_name='Last name 1',
#             first_name='First name 1'
#             )
#         self.user2 = User.objects.create(
#             username='user2'
#             )
#         self.user3 = User.objects.create(
#             username='user3'
#             )
#         self.shop = Shop.objects.create(
#             name='Shop name',
#             description='Shop description'
#             )
#         self.pu1 = ProductUnit.objects.create(
#             name='pu1 name',
#             description='pu1 description',
#             unit='CL',
#             type='keg'
#             )
#         self.pu2 = ProductUnit.objects.create(
#             name='pu2 name',
#             description='pu2 description',
#             unit='G',
#             type='meat'
#             )
#         self.pb1 = ProductBase.objects.create(
#             name='pb1 name',
#             description='pb1 description',
#             manual_price=1.15,
#             brand='pb1 brand',
#             type='single_product',
#             shop=self.shop
#             )
#         self.pb2 = ProductBase.objects.create(
#             name='pb2 name',
#             description='pb2 description',
#             manual_price=150,
#             brand='pb2 brand',
#             type='container',
#             quantity=100,
#             product_unit=self.pu1,
#             shop=self.shop
#             )
#         self.pb3 = ProductBase.objects.create(
#             name='pb3 name',
#             description='pb3 description',
#             manual_price=150,
#             brand='pb3 brand',
#             type='container',
#             quantity=100,
#             product_unit=self.pu2,
#             shop=self.shop
#             )
#         self.pb4 = ProductBase.objects.create(
#             name='pb4 name',
#             description='pb4 description shooter',
#             manual_price=1.15,
#             brand='pb4 brand',
#             type='single_product',
#             shop=self.shop
#             )
#         self.lydia_user1 = Lydia.objects.create(
#             amount=10,
#             id_from_lydia='abcdefg',
#             sender=self.user1,
#             recipient=self.user2
#             )
#         self.cash_user3 = Cash.objects.create(
#             amount=6,
#             sender=self.user3,
#             recipient=self.user2
#             )
#         self.payment = Payment.objects.create()
#         self.payment.lydias.add(self.lydia_user1)
#         self.payment.cashs.add(self.cash_user3)
#         self.payment.maj_amount()
#         self.sale = Sale.objects.create(
#             wording='',
#             sender=self.user1,
#             recipient=self.user2,
#             operator=self.user1,
#             payment=self.payment
#             )
#         self.sp_pb1 = SingleProduct.objects.create(
#             price=1,
#             purchase_date='2016-01-01',
#             place='place sp',
#             product_base=self.pb1,
#             sale_price=1,
#             sale=self.sale,
#             is_sold=True
#             )
#         self.c_pb2 = Container.objects.create(
#             price=100,
#             purchase_date='2016-01-01',
#             place='place sp',
#             product_base=self.pb2
#             )
#         self.spfc_pb2 = SingleProductFromContainer.objects.create(
#             quantity=10,
#             container=self.c_pb2,
#             sale_price=15,
#             sale=self.sale
#             )
#
#     def test__str__(self):
#         self.assertEqual(
#             self.sale.__str__(),
#             'Achat n°' + str(self.sale.pk)
#         )
#
#     def test_list_single_products(self):
#         self.assertCountEqual(
#             self.sale.list_single_products()[0],
#             [self.sp_pb1]
#         )
#         self.assertAlmostEqual(
#             self.sale.list_single_products()[1],
#             decimal.Decimal(1)
#         )
#
#     def test_list_single_products_from_container(self):
#         self.assertCountEqual(
#             self.sale.list_single_products_from_container()[0],
#             [self.spfc_pb2]
#         )
#         self.assertAlmostEqual(
#             self.sale.list_single_products_from_container()[1],
#             decimal.Decimal(15)
#         )
#
#     def test_maj_amount(self):
#         self.assertAlmostEqual(
#             self.sale.amount,
#             decimal.Decimal(0)
#         )
#         self.sale.maj_amount()
#         self.assertAlmostEqual(
#             self.sale.amount,
#             decimal.Decimal(16)
#         )
#
#     def test_price_for(self):
#         self.assertAlmostEqual(
#             self.sale.price_for(self.user1),
#             decimal.Decimal(-10)
#         )
#         self.assertAlmostEqual(
#             self.sale.price_for(self.user2),
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             self.sale.price_for(self.user3),
#             decimal.Decimal(-6)
#         )
#
#     def test_string_products(self):
#         self.assertEqual(
#             self.sale.string_products(),
#             self.sp_pb1.__str__() + ', ' + self.spfc_pb2.__str__()
#         )
#
#
# class MiscellaneousSaleTransfertTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.user2 = User.objects.create(
#             username='user2',
#             balance=10
#             )
#         sale_transfert(
#             sender=self.user1,
#             recipient=self.user2,
#             amount=50,
#             date=datetime.date.today(),
#             justification='remboursement'
#         )
#
#     def test_debit_balance(self):
#         # Exceptions are directly raised if objects does not exists
#         debit_balance = DebitBalance.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             debit_balance.amount,
#             decimal.Decimal(50)
#         )
#         self.assertEqual(
#             debit_balance.sender,
#             self.user1
#         )
#         self.assertEqual(
#             debit_balance.recipient,
#             self.user2
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(50)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             [DebitBalance.objects.get(sender=self.user1)]
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(50)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(50)
#         )
#         self.assertTrue(sale.done)
#         self.assertFalse(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'transfert'
#         )
#         self.assertEqual(
#             sale.wording,
#             ''
#         )
#         self.assertEqual(
#             sale.justification,
#             'remboursement'
#         )
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             self.user2
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user1
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(50)
#         )
#         self.assertAlmostEqual(
#             self.user2.balance,
#             decimal.Decimal(60)
#         )
#
#
# class MiscellaneousSaleRechargingSelfLydiaTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.lydia = Lydia.objects.create(
#             date_operation=datetime.date.today(),
#             amount=10,
#             id_from_lydia='abcdefg',
#             sender=self.user1,
#             recipient=User.objects.get(username='AE_ENSAM')
#             )
#         sale_recharging(
#             sender=self.user1,
#             operator=self.user1,
#             date=datetime.date.today(),
#             wording='Rechargement automatique',
#             payments_list=[self.lydia]
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(10)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             [self.lydia]
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             []
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(10)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(0)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(10)
#         )
#         self.assertTrue(sale.done)
#         self.assertTrue(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'recharging'
#         )
#         self.assertEqual(
#             sale.wording,
#             'Rechargement automatique'
#         )
#         self.assertIsNone(sale.justification)
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user1
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_product(self):
#         spfc = SingleProductFromContainer.objects.all()[0]
#         self.assertEqual(
#             spfc.quantity,
#             1000
#         )
#         self.assertEqual(
#             spfc.sale_price,
#             10
#         )
#         self.assertEqual(
#             spfc.container,
#             Container.objects.get(pk=1)
#         )
#         self.assertEqual(
#             spfc.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(110)
#         )
#
#
# class MiscellaneousSaleRechargingWithOperatorTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.user2 = User.objects.create(
#             username='user2'
#             )
#         self.cash = Cash.objects.create(
#             amount=10,
#             sender=self.user1,
#             recipient=self.user2
#             )
#         sale_recharging(
#             sender=self.user1,
#             operator=self.user2,
#             date=datetime.date.today(),
#             wording='Rechargement manuel',
#             payments_list=[self.cash]
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(10)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             [self.cash]
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             []
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(10)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(0)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(10)
#         )
#         self.assertTrue(sale.done)
#         self.assertTrue(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'recharging'
#         )
#         self.assertEqual(
#             sale.wording,
#             'Rechargement manuel'
#         )
#         self.assertIsNone(sale.justification)
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user2
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_product(self):
#         spfc = SingleProductFromContainer.objects.all()[0]
#         self.assertEqual(
#             spfc.quantity,
#             1000
#         )
#         self.assertEqual(
#             spfc.sale_price,
#             10
#         )
#         self.assertEqual(
#             spfc.container,
#             Container.objects.get(pk=1)
#         )
#         self.assertEqual(
#             spfc.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(110)
#         )
#
#
# class MiscellaneousSaleExceptionnalCreditTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.user2 = User.objects.create(
#             username='user2',
#             balance=10
#             )
#         sale_exceptionnal_movement(
#             operator=self.user2,
#             affected=self.user1,
#             is_credit=True,
#             amount=10,
#             date=datetime.date.today(),
#             justification='Exception'
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(10)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             []
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(0)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(10)
#         )
#         self.assertTrue(sale.done)
#         self.assertTrue(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'exceptionnal_movement'
#         )
#         self.assertEqual(
#             sale.wording,
#             'Mouvement exceptionnel'
#         )
#         self.assertEqual(
#             sale.justification,
#             'Exception'
#         )
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user2
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_product(self):
#         spfc = SingleProductFromContainer.objects.all()[0]
#         self.assertEqual(
#             spfc.quantity,
#             1000
#         )
#         self.assertEqual(
#             spfc.sale_price,
#             10
#         )
#         self.assertEqual(
#             spfc.container,
#             Container.objects.get(pk=1)
#         )
#         self.assertEqual(
#             spfc.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(110)
#         )
#
#
# class MiscellaneousSaleExceptionnalDebitTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.user2 = User.objects.create(
#             username='user2',
#             balance=10
#             )
#         sale_exceptionnal_movement(
#             operator=self.user2,
#             affected=self.user1,
#             is_credit=False,
#             amount=10,
#             date=datetime.date.today(),
#             justification='Exception'
#         )
#
#     def test_debit_balance(self):
#         debit_balance = DebitBalance.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             debit_balance.amount,
#             decimal.Decimal(10)
#         )
#         self.assertEqual(
#             debit_balance.sender,
#             self.user1
#         )
#         self.assertEqual(
#             debit_balance.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(10)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             [DebitBalance.objects.all()[0]]
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(10)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(10)
#         )
#         self.assertTrue(sale.done)
#         self.assertFalse(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'exceptionnal_movement'
#         )
#         self.assertEqual(
#             sale.wording,
#             'Mouvement exceptionnel'
#         )
#         self.assertEqual(
#             sale.justification,
#             'Exception'
#         )
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user2
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_product(self):
#         spfc = SingleProductFromContainer.objects.all()[0]
#         self.assertEqual(
#             spfc.quantity,
#             1000
#         )
#         self.assertEqual(
#             spfc.sale_price,
#             10
#         )
#         self.assertEqual(
#             spfc.container,
#             Container.objects.get(pk=1)
#         )
#         self.assertEqual(
#             spfc.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(90)
#         )
#
#
# class MiscellaneousDirectSaleTestCase(TestCase):
#     fixtures = ['shops.json', 'special_members.json']
#
#     def setUp(self):
#         self.user1 = User.objects.create(
#             username='user1',
#             balance=100
#             )
#         self.shop = Shop.objects.create(
#             name='Shop name',
#             description='Shop description'
#             )
#         self.pu1 = ProductUnit.objects.create(
#             name='pu1 name',
#             description='pu1 description',
#             unit='CL',
#             type='keg'
#             )
#         self.pb1 = ProductBase.objects.create(
#             name='pb1 name',
#             description='pb1 description',
#             manual_price=1.15,
#             brand='pb1 brand',
#             type='single_product',
#             shop=self.shop
#             )
#         self.pb2 = ProductBase.objects.create(
#             name='pb2 name',
#             description='pb2 description',
#             manual_price=150,
#             brand='pb2 brand',
#             type='container',
#             quantity=100,
#             product_unit=self.pu1,
#             shop=self.shop
#             )
#         self.sp_pb1 = SingleProduct.objects.create(
#             price=1,
#             purchase_date='2016-01-01',
#             place='place sp',
#             product_base=self.pb1,
#             sale_price=1,
#             is_sold=True
#             )
#         self.c_pb2 = Container.objects.create(
#             price=100,
#             purchase_date='2016-01-01',
#             place='place sp',
#             product_base=self.pb2
#             )
#         self.spfc_pb2 = SingleProductFromContainer.objects.create(
#             quantity=10,
#             container=self.c_pb2,
#             sale_price=15,
#             )
#         sale_sale(
#             sender=self.user1,
#             operator=self.user1,
#             date=datetime.date.today(),
#             wording='Vente Shop name',
#             products_list=[self.sp_pb1, self.spfc_pb2]
#         )
#
#     def test_debit_balance(self):
#         debit_balance = DebitBalance.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             debit_balance.amount,
#             decimal.Decimal(16)
#         )
#         self.assertEqual(
#             debit_balance.sender,
#             self.user1
#         )
#         self.assertEqual(
#             debit_balance.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#
#     def test_payment(self):
#         # Exceptions are directly raised if objects does not exists
#         payment = Payment.objects.all()[0]  # Theorically the only one.
#         self.assertAlmostEqual(
#             payment.amount,
#             decimal.Decimal(16)
#         )
#         self.assertCountEqual(
#             payment.list_cheque()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_lydia()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_cash()[0],
#             []
#         )
#         self.assertCountEqual(
#             payment.list_debit_balance()[0],
#             [DebitBalance.objects.all()[0]]
#         )
#         self.assertAlmostEqual(
#             payment.list_cheque()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_lydia()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_cash()[1],
#             decimal.Decimal(0)
#         )
#         self.assertAlmostEqual(
#             payment.list_debit_balance()[1],
#             decimal.Decimal(16)
#         )
#
#     def test_sale(self):
#         # Exceptions are directly raised if objects does not exists
#         sale = Sale.objects.get(sender=self.user1)
#         self.assertAlmostEqual(
#             sale.amount,
#             decimal.Decimal(16)
#         )
#         self.assertTrue(sale.done)
#         self.assertFalse(sale.is_credit)
#         self.assertEqual(
#             sale.category,
#             'sale'
#         )
#         self.assertEqual(
#             sale.wording,
#             'Vente Shop name'
#         )
#         self.assertIsNone(sale.justification)
#         self.assertEqual(
#             sale.sender,
#             self.user1
#         )
#         self.assertEqual(
#             sale.recipient,
#             User.objects.get(username='AE_ENSAM')
#         )
#         self.assertEqual(
#             sale.operator,
#             self.user1
#         )
#         self.assertEqual(
#             sale.payment,
#             Payment.objects.all()[0]
#         )
#
#     def test_products(self):
#         self.assertEqual(
#             self.sp_pb1.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#         self.assertTrue(self.sp_pb1.is_sold)
#         self.assertEqual(
#             self.spfc_pb2.sale,
#             Sale.objects.get(sender=self.user1)
#         )
#
#     def test_balances(self):
#         self.assertAlmostEqual(
#             self.user1.balance,
#             decimal.Decimal(84)
#         )


class SharedEventTestCase(TestCase):
    def setUp(self):
        self.manager = User.objects.create(
            username='username_manager',
            last_name='Last name manager',
            first_name='First name manager'
        )

        self.event1 = SharedEvent.objects.create(
            description='Test53',
            date=datetime.date(2053, 1, 1),
            manager=self.manager,
            price=decimal.Decimal(1000.00)
        )
        self.user1 = User.objects.create(
            username='user1',
            last_name='Last name 1',
            first_name='First name 1',
            balance=1000
        )
        self.user2 = User.objects.create(
            username='user2',
            last_name='Last name 2',
            first_name='First name 2',
            balance=2000
        )
        self.user3 = User.objects.create(
            username='user3',
            last_name='Last name 3',
            first_name='First name 3',
            balance=3000
        )
        self.user4 = User.objects.create(
            username='user4',
            last_name='Last name 4',
            first_name='First name 4',
            balance=4000
        )
        self.banker = User.objects.create(
            username='Banker',
            last_name='Ker',
            first_name='Ban',
            balance=0
        )

    def test_wording(self):
        self.assertEqual(self.event1.wording(), "Événement : Test53, le 01/01")

    def test_add_and_remove_user(self):
        # INIT
        self.event1.change_weight(self.user1, 100, isParticipant=True)
        self.event1.change_weight(self.user1, 30, isParticipant=True)
        self.event1.add_weight(self.user1, 23, isParticipant=True)
        self.event1.change_weight(self.user1, 10, isParticipant=False)
        self.event1.change_weight(self.user1, 1, isParticipant=False)
        self.event1.add_weight(self.user1, 2, isParticipant=False)
        # User 1 now should have 3 in registration, and 53 in participation
        self.event1.add_weight(self.user2, 200, isParticipant=False)
        self.event1.add_weight(self.user2, 2, isParticipant=False)
        # User 2 now should have 202 in registration
        self.event1.add_weight(self.user3, 400, isParticipant=True)
        self.event1.change_weight(self.user3, 47, isParticipant=True)
        # User 3 now should have 303 in participation
        registration_u1 = self.event1.get_weight_of_user(
            self.user1, isParticipant=False)
        participation_u1 = self.event1.get_weight_of_user(
            self.user1, isParticipant=True)
        registration_u2 = self.event1.get_weight_of_user(
            self.user2, isParticipant=False)
        participation_u2 = self.event1.get_weight_of_user(
            self.user2, isParticipant=True)
        registration_u3 = self.event1.get_weight_of_user(
            self.user3, isParticipant=False)
        participation_u3 = self.event1.get_weight_of_user(
            self.user3, isParticipant=True)
        registration_u4 = self.event1.get_weight_of_user(
            self.user4, isParticipant=False)
        participation_u4 = self.event1.get_weight_of_user(
            self.user4, isParticipant=True)

        # TESTS
        self.assertEqual(registration_u1, 3)
        self.assertEqual(participation_u1, 53)

        self.assertEqual(registration_u2, 202)
        self.assertEqual(participation_u2, 0)

        self.assertEqual(registration_u3, 0)
        self.assertEqual(participation_u3, 47)

        self.assertEqual(registration_u4, 0)
        self.assertEqual(participation_u4, 0)

        # END
        self.event1.remove_user(self.user1)
        self.event1.remove_user(self.user2)
        self.event1.remove_user(self.user3)
        self.event1.remove_user(self.user4)

        self.assertEqual(self.event1.get_weight_of_user(
            self.user1, isParticipant=False), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user1, isParticipant=True), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user2, isParticipant=False), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user2, isParticipant=True), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user3, isParticipant=False), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user3, isParticipant=True), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user4, isParticipant=False), 0)
        self.assertEqual(self.event1.get_weight_of_user(
            self.user4, isParticipant=True), 0)

    def test_get_price_of_user(self):
        # INIT
        self.event1.change_weight(self.user1, 9, True)
        self.event1.change_weight(self.user2, 1, True)
        # TESTS
        # Reminder: price = 1000
        self.assertEqual(self.event1.get_price_of_user(self.user1), 900)
        self.assertEqual(self.event1.get_price_of_user(self.user2), 100)
        # END
        self.event1.remove_user(self.user1)
        self.event1.remove_user(self.user2)

    def test_get_total_weights(self):
        # INIT
        self.event1.change_weight(self.user1, 10, isParticipant=True)
        self.event1.change_weight(self.user1, 5, isParticipant=False)
        self.event1.change_weight(self.user2, 40, isParticipant=True)
        self.event1.change_weight(self.user2, 25, isParticipant=False)
        # TESTS
        self.assertEqual(self.event1.get_total_weights_registrants(), 30)
        self.assertEqual(self.event1.get_total_weights_participants(), 50)
        # END
        self.event1.remove_user(self.user1)
        self.event1.remove_user(self.user2)

    def test_get_total_users(self):
        # INIT
        self.event1.change_weight(self.user1, 10, isParticipant=True)
        self.event1.change_weight(self.user1, 5, isParticipant=False)
        self.event1.change_weight(self.user2, 40, isParticipant=True)
        # TESTS
        self.assertEqual(self.event1.get_number_registrants(), 1)
        self.assertEqual(self.event1.get_number_participants(), 2)
        # END
        self.event1.remove_user(self.user1)
        self.event1.remove_user(self.user2)

    def test_pay_by_total(self):
        # INIT
        event_total_price = SharedEvent.objects.create(
            description='Test_payment',
            date=datetime.date(2053, 1, 1),
            manager=self.manager,
            price=decimal.Decimal(1000.00)
        )
        user1_initial_balance = self.user1.balance
        user2_initial_balance = self.user2.balance
        banker_initial_balance = self.banker.balance

        event_total_price.change_weight(self.user1, 10, isParticipant=True)
        event_total_price.change_weight(self.user2, 5, isParticipant=False)
        event_total_price.change_weight(self.user2, 40, isParticipant=True)
        event_total_price.pay_by_total(self.manager, self.banker, decimal.Decimal(100.00))

        # Get users with updated balance
        self.user1 = User.objects.get(pk=self.user1.pk)
        self.user2 = User.objects.get(pk=self.user2.pk)

        # TESTS
        self.assertEqual(event_total_price.done, True)
        self.assertEqual(event_total_price.payment_by_ponderation, False)
        self.assertEqual(self.banker.balance, banker_initial_balance + 100)
        self.assertEqual(event_total_price.price, 100)
        self.assertEqual(
            event_total_price.remark, 'Paiement par Borgia (Prix total : 100)')
        self.assertEqual(self.user1.balance, user1_initial_balance - 20)
        self.assertEqual(self.user2.balance, user2_initial_balance - 80)

    def test_pay_by_ponderation(self):
        # INIT
        event_pond_price = SharedEvent.objects.create(
            description='Test_payment',
            date=datetime.date(2053, 1, 1),
            manager=self.manager,
            price=decimal.Decimal(150.0)
        )
        user1_initial_balance = self.user1.balance
        user2_initial_balance = self.user2.balance
        banker_initial_balance = self.banker.balance

        event_pond_price.change_weight(self.user1, 10, isParticipant=True)
        event_pond_price.change_weight(self.user2, 5, isParticipant=False)
        event_pond_price.change_weight(self.user2, 40, isParticipant=True)
        event_pond_price.pay_by_ponderation(self.manager, self.banker, 3)

        # Get users with updated balance
        self.user1 = User.objects.get(pk=self.user1.pk)
        self.user2 = User.objects.get(pk=self.user2.pk)

        # TESTS
        self.assertEqual(event_pond_price.done, True)
        self.assertEqual(event_pond_price.payment_by_ponderation, True)
        self.assertEqual(event_pond_price.price, decimal.Decimal(3.00))
        self.assertEqual(self.banker.balance, banker_initial_balance + 150)
        self.assertEqual(
            event_pond_price.remark, 'Paiement par Borgia (Prix par pondération: 3)')
        self.assertEqual(self.user1.balance, user1_initial_balance - 30)
        self.assertEqual(self.user2.balance, user2_initial_balance - 120)