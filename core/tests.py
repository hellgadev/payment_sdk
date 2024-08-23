import asyncio
import unittest
from unittest.mock import patch, AsyncMock

import websockets

from core.sdk import PaymentSDK
from core.utils.exceptions import PaymentException
from core.ws import PaymentWebSocketClient


class TestPaymentSDK(unittest.TestCase):
    def setUp(self):
        self.sdk = PaymentSDK(api_key="valid_api_key")

    def test_successful_credit_card_payment(self):
        with self.assertLogs(level='INFO') as log:
            self.sdk.process_payment("credit_card", 100.0, "USD")
            self.assertIn("INFO:root:Credit Card core of 100.00 USD success.", log.output)

    def test_successful_paypal_payment(self):
        with self.assertLogs(level='INFO') as log:
            self.sdk.process_payment("paypal", 50.0, "EUR")
            self.assertIn("INFO:root:PayPal core of 50.00 EUR success.", log.output)

    def test_successful_crypto_payment(self):
        with self.assertLogs(level='INFO') as log:
            self.sdk.process_payment("crypto", 1.5, "BTC")
            self.assertIn("INFO:root:Crypto core of 1.50 BTC success.", log.output)

    def test_invalid_payment_method(self):
        with self.assertLogs(level='INFO') as log:
            self.sdk.process_payment("invalid_method", 100.0, "USD")
            self.assertIn("ERROR:root:Invalid core method: invalid_method", log.output)

    @patch('core.sdk.PaymentService.process_payment')
    def test_payment_fails_due_to_exception(self, mock_process_payment):
        mock_process_payment.side_effect = PaymentException("Credit Card core failed due to network error.")
        with self.assertLogs(level='INFO') as log:
            self.sdk.process_payment("credit_card", 100.0, "USD")
            self.assertIn("ERROR:root:Credit Card core failed due to network error.", log.output)

    def test_invalid_api_key(self):
        with self.assertLogs(level='INFO') as log:
            sdk_with_invalid_key = PaymentSDK(api_key="invalid_key")
            sdk_with_invalid_key.process_payment("credit_card", 100.0, "USD")
            self.assertIn("ERROR:root:Invalid API key. Cannot process core.", log.output)

    def test_default_currency(self):
        with self.assertLogs(level='INFO') as log:
            sdk_with_default_currency = PaymentSDK(api_key="valid_api_key", default_currency="GBP")
            sdk_with_default_currency.process_payment("paypal", 100.0)
            self.assertIn("INFO:root:PayPal core of 100.00 GBP success.", log.output)


class TestPaymentWebSocketClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.uri = 'wss://echo.websocket.org'
        self.client = PaymentWebSocketClient(uri=self.uri)

    @patch('websockets.connect', new_callable=AsyncMock)
    async def test_reconnect_on_connection_error(self, mock_connect):
        # Simulate connection error
        mock_connect.side_effect = [AsyncMock(), ConnectionError("Connection failed")]

        loop = asyncio.get_event_loop()

        # Run the client in a separate task
        task = loop.create_task(self.client.connect())

        await asyncio.sleep(2)

        self.assertEqual(mock_connect.call_count, 2)

        task.cancel()

        with self.assertRaises(asyncio.CancelledError):
            await task


if __name__ == "__main__":
    unittest.main()
