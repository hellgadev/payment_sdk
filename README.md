## Test task
### ABOUT: 
This is a payment processing system (SDK) that supports multiple payment methods (e.g., Credit Card, PayPal, crypto, etc). 
When the service is executed, it prints the data to the console (example: "Credit Card payment success").

### Done:
* SDK Implementation: The main SDK code is located in core/sdk.py. 
  * SDK API Access: The SDK can be accessed via the API at POST /api/v1/pay/. The request data should include {'method': str, 'amount': float, 'currency': str}.
* WebSocket Client: The WebSocket client is implemented in core/ws.py. 
* Unit Tests: Unit tests are provided for both the SDK and the WebSocket client