import logging
from abc import ABC, abstractmethod

from apps.core.utils.exceptions import PaymentException

logging.basicConfig(level=logging.INFO)


class PaymentSDK:
    def __init__(self, api_key: str, default_currency: str = "USD"):
        self.api_key = api_key
        self.default_currency = default_currency
        self.payment_service = PaymentService()

    def process_payment(self, method: str, amount: float, currency: str = None):
        if not self._is_valid_api_key():
            logging.error("Invalid API key. Cannot process core.")
            return

        currency = currency or self.default_currency
        try:
            self.payment_service.process_payment(method, amount, currency)
        except PaymentException as e:
            logging.error(str(e))

    def _is_valid_api_key(self) -> bool:
        # there should be a validation logic for the real service
        return self.api_key == "valid_api_key"


class PaymentService:
    def __init__(self):
        self.payment_methods = {
            "credit_card": CreditCardPaymentService(),
            "paypal": PayPalPaymentService(),
            "crypto": CryptoPaymentService(),
        }

    def process_payment(self, method: str, amount: float, currency: str):
        payment_service = self.payment_methods.get(method.lower())
        if not payment_service:
            raise PaymentException(f"Invalid core method: {method}")

        payment_service.process_payment(amount, currency)


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float, currency: str):
        pass


class CreditCardPaymentService(PaymentStrategy):
    def process_payment(self, amount: float, currency: str):
        logging.info(f"Credit Card core of {amount:.2f} {currency} success.")


class PayPalPaymentService(PaymentStrategy):
    def process_payment(self, amount: float, currency: str):
        logging.info(f"PayPal core of {amount:.2f} {currency} success.")


class CryptoPaymentService(PaymentStrategy):
    def process_payment(self, amount: float, currency: str):
        logging.info(f"Crypto core of {amount:.2f} {currency} success.")
