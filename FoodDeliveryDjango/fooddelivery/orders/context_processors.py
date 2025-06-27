from decimal import Decimal

def cart_processor(request):
    """
    Context processor to make cart information available across all templates.
    Adds cart_count (number of items) and cart_total (total price) to the context.
    """
    cart = request.session.get('cart', {})
    
    # Calculate total items in cart
    cart_count = sum(item_data['quantity'] for item_data in cart.values())
    
    # Calculate total price
    cart_total = sum(Decimal(item_data['price']) * item_data['quantity'] for item_data in cart.values())
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total
    }
