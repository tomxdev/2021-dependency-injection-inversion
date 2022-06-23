import unittest
from unittest.mock import patch
from final import *


class AuthorizerSMS_TestCase(unittest.TestCase):
    def test_init_authorized(self):
        auth = AuthorizerSMS()
        self.assertFalse(auth.is_authorized())

    def test_code_decimal(self):
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        self.assertTrue(auth.code.isdecimal())

    def test_authorize_success(self):
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        with patch('builtins.input', return_value=auth.code):
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    @patch('builtins.input', return_value='1234567')
    def test_authorize_fail(self, mocked_input):
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        auth.authorize()
        self.assertFalse(auth.is_authorized())


class AuthorizerRobot_TestCase(unittest.TestCase):
    def test_init_authorized(self):
        auth = AuthorizerRobot()
        self.assertFalse(auth.is_authorized())

    def test_authorize_success(self):
        with patch('builtins.input', return_value='n'):
            auth = AuthorizerRobot()
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    def test_authorize_success_uppercase(self):
        with patch('builtins.input', return_value="N"):
            auth = AuthorizerRobot()
            auth.authorize()
            self.assertTrue(auth.is_authorized())

    def test_authorize_fail(self):
        with patch('builtins.input', return_value='y'):
            auth = AuthorizerRobot()
            auth.authorize()
            self.assertFalse(auth.is_authorized())


class PaymentProcessor_TestCase(unittest.TestCase):
    def test_init(self):
        auth = AuthorizerSMS()
        p = PaymentProcessor(auth)
        self.assertEqual(p.authorizer, auth)

    def test_payment_success(self):
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        with patch('builtins.input', return_value=auth.code):
            p = PaymentProcessor(auth)
            order = Order()
            p.pay(order)
            self.assertEqual(order.status, 'paid')

    def test_payment_fail(self):
        auth = AuthorizerSMS()
        auth.generate_sms_code()
        with patch('builtins.input', return_value='1234567'):
            p = PaymentProcessor(auth)
            order = Order()
            self.assertRaises(Exception, p.pay, order)


if __name__ == '__main__':
    unittest.main()
