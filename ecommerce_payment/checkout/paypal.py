import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

# to make connection to paypal
class PayPalClient:
    def __init__(self):
        self.client_id = 'AROpKu1l5sIPjsyx2Ec08IbGgCkTZetuexJzVAMff5gvL3JHfH7GytLiP1b4ihgQ9VLVajuz_P_oqmlj'
        self.client_secret = 'EEtR5fJw8xfqhntLPhF_0DOUbDZB5RIMhpMUZ-OHCgqzcR1xJlL9O1QfwnxYMJnDWf8ZMin_8ANzqdRP'
        self.environment = SandboxEnvironment(client_id = self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)

