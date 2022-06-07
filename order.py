"""
Order functionality with SOLID examples

S:
 - Single responsibility
 - Order class has SINGLE responsibility of holding info about order
 - PaymentProcessor has SINGLE responsibility to process Order
 - WATCHOUT for creating coupling between Order and Payment


O:
 - Open/Closed
 - The code should be opened for new functionality
 - The code should be closed for the modification, so changes does not destroy everything
 - Example we can have Payment processor with 2 methods, pay_debit and pay_credit. To add new function like pay_crypto
   we would need create completely new method and do some refactoring which violates Close principle, because we would
   need to modify existing PaymentProcessor class by adding new function to it. Thus we need to use
   abstraction to multiple classes. In this way we do not need to change any existing code to add new functionality.


L:
 - Liskov substitution
 - You should be able to replace objects with their subclases without breaking the code
 - Example lets say that the payment processors have different types of parameters for the pay method. Debit and credit
   use security_code and crypto valet_id. Thus to not to break the code by creating the crypto payment processor we
   need to pass parameters in different way. One of the solutions is to use initialization.

I:
 - Interface segregation principle
 - It is better to have more interfaces rather than one master interface.
 - Example issue : we have 3 types of payment processors. 2 of them use MFA authorization and third does not.
 - To adhere to this principle we can have 2 approaches. Either branch out our dependency where we would have 2
   abstract parent classes. Root would be without, then it would have subclass Abstract+MFA and then we can implement
   from class we need. Alternatively, we can use composition to have basically 2 interfaces. 1 as the payment proccessor
   2nd as MFA authorizer. Thus having 2 interfaces for payment processing.

D:
 - Dependency inversion
 - This means that if we do any kind of composition (e.g. PaymentProcessor + Order, or PaymentProcessor + Authorizer)
   we are introducing tight coupling. To avoid that we should depend on ABSTRACT rather then concrete classes.

"""
import dataclasses
from abc import ABC


@dataclasses
class Order():
    order_id: str
    user_id: str
    items: list
    status: str
    total_cost: int


class Authorizer(ABC):
    def authorize(self,order, code) -> bool:
        raise NotImplemented

class AuthorizerMFA(Authorizer):
    def authorize(self,order, code):
        print(f"MFA authorization check with code {code}")
        return code is not None

class AuthorizerSMS(Authorizer):
    def authorize(self,order, code):
        print(f"SMS authorization check with code {code}")
        return order.items > 0 and code is not None

class PaymentProcessor(ABC):

    def __init__(self, authorizer:Authorizer):
        self.auth = authorizer

    def pay(self, order):
        """

        :param order:
        :param security_code:
        :return:
        """
        raise NotImplemented

class PaymentProcessorCredit(PaymentProcessor):
    def __init__(self, security_code: str, authorizer: Authorizer):
        super().__init__(authorizer)
        self.security_code = security_code

    def pay(self,order: Order):
        """

        :param order:
        :return:
        """
        print(f"Paying by credit for order {order}")
        print(f"Verifying order with code {self.security_code}")
        print(f"Payment authorizer {self.auth.authorize(order, self.security_code)}")

        order.status = "paid"

class PaymentProcessorDebet(PaymentProcessor):
    def __init__(self, security_code, authorizer: Authorizer):
        super().__init__(authorizer)
        self.security_code = security_code

    def pay_debit(self,order):
        """
        :param order:
        :return:
        """
        print(f"Paying by debit for order {order}")
        print(f"Verifying order with code {self.security_code}")
        print(f"Payment authorizer {self.auth.authorize(order, self.security_code)}")
        order.status = "paid"


class PaymentProcessorCrypto(PaymentProcessor):
    def __init__(self, valet_id, authorizer: Authorizer):
        super().__init__(authorizer)
        self.valet_id = valet_id

    def pay_debit(self, order):
        """
        :param order:
        :return:
        """
        print(f"Paying by crypto for order {order}")
        print(f"Verifying order with valet_id {self.valet_id}")
        print(f"Payment authorizer {self.auth.authorize(order, self.valet_id)}")

        order.status = "paid"


