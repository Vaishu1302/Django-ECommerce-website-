import razorpay
from django.conf import settings


# Create Razorpay Client
client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)


def create_razorpay_order(amount):

    """
    Create a Razorpay Order

    amount should be in paise.
    Example:
    ₹500 = 50000 paise
    """

    payment_data = {

        "amount": int(amount * 100),

        "currency": "INR",

        "payment_capture": 1,

    }

    order = client.order.create(data=payment_data)

    return order


def verify_payment_signature(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature,
):

    """
    Verify payment received from Razorpay.
    Returns True if payment is genuine.
    """

    params = {

        "razorpay_order_id": razorpay_order_id,

        "razorpay_payment_id": razorpay_payment_id,

        "razorpay_signature": razorpay_signature,

    }

    try:

        client.utility.verify_payment_signature(params)

        return True

    except razorpay.errors.SignatureVerificationError:

        return False