from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal
from .models import Order, OrderItem
from restaurants.models import Restaurant, MenuItem
from .forms import CheckoutForm

def add_to_cart(request):
    """Add a menu item to the shopping cart."""
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Get the menu item
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
        # Initialize cart if needed
        cart = request.session.get('cart', {})
        
        # Check if we already have this item in cart
        if menu_item_id in cart:
            # Update quantity
            cart[menu_item_id]['quantity'] += quantity
        else:
            # Add new item to cart
            cart[menu_item_id] = {
                'quantity': quantity,
                'price': str(menu_item.price)
            }
        
        # Save back to session
        request.session['cart'] = cart
        
        # Redirect back to restaurant page
        messages.success(request, f'Added {menu_item.name} to your cart!')
        return redirect('restaurant_detail', restaurant_id=menu_item.category.restaurant.id)
    
    # If not POST, redirect to home
    return redirect('home')

def update_cart(request):
    """Update quantities or remove items from the cart."""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        # Loop through all items in the form
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                # Extract menu item ID from the field name
                item_id = key.replace('quantity_', '')
                quantity = int(value)
                
                if quantity > 0:
                    # Update quantity
                    if item_id in cart:
                        cart[item_id]['quantity'] = quantity
                else:
                    # Remove item if quantity is 0
                    if item_id in cart:
                        del cart[item_id]
            
            elif key.startswith('remove_'):
                # Handle removal buttons
                item_id = key.replace('remove_', '')
                if item_id in cart:
                    del cart[item_id]
        
        # Save updated cart back to session
        request.session['cart'] = cart
        
        messages.success(request, 'Cart updated successfully!')
    
    return redirect('cart')

def cart(request):
    """Display the shopping cart contents."""
    cart = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')
    restaurant_id = None
    
    if cart:
        # Get details for each item in cart
        for item_id, item_data in cart.items():
            menu_item = get_object_or_404(MenuItem, id=item_id)
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            item_total = price * quantity
            
            items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'price': price,
                'item_total': item_total
            })
            
            total += item_total
            
            # Store restaurant ID for the "Continue Shopping" link
            if restaurant_id is None:
                restaurant_id = menu_item.category.restaurant.id
    
    context = {
        'cart_items': items,
        'total': total,
        'restaurant_id': restaurant_id
    }
    
    return render(request, 'orders/cart.html', context)

@login_required
def checkout(request):
    """Handle the checkout process."""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Get cart items and calculate total
    items = []
    total = Decimal('0.00')
    restaurant = None
    
    # Process all items in cart
    for item_id, item_data in cart.items():
        menu_item = get_object_or_404(MenuItem, id=item_id)
        quantity = item_data['quantity']
        price = Decimal(item_data['price'])
        item_total = price * quantity
        
        items.append({
            'menu_item': menu_item,
            'quantity': quantity,
            'price': price,
            'item_total': item_total
        })
        
        total += item_total
        
        # Get restaurant (all items must be from the same restaurant)
        if restaurant is None:
            restaurant = menu_item.category.restaurant
        elif restaurant.id != menu_item.category.restaurant.id:
            messages.error(request, 'Items in your cart are from different restaurants!')
            return redirect('cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create the order
            order = Order(
                user=request.user,
                restaurant=restaurant,
                total_amount=total,
                delivery_address=form.cleaned_data['delivery_address'],
                contact_phone=form.cleaned_data['contact_phone'],
                payment_method=form.cleaned_data['payment_method'],
                delivery_instructions=form.cleaned_data['delivery_instructions'],
                status='pending'
            )
            order.save()
            
            # Create order items
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item['menu_item'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Clear the cart
            del request.session['cart']
            
            # Redirect to order confirmation
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        # Initial form - try to pre-fill with user's default address if available
        initial_data = {}
        if hasattr(request.user, 'profile'):
            default_address = request.user.profile.addresses.filter(is_default=True).first()
            if default_address:
                initial_data['delivery_address'] = str(default_address)
                initial_data['contact_phone'] = request.user.profile.phone_number
        
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': items,
        'total': total,
        'restaurant': restaurant
    }
    
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    """Display the order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order
    }
    
    return render(request, 'orders/order_confirmation.html', context)

@login_required
def order_history(request):
    """Display the user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_id):
    """Display details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order
    }
    
    return render(request, 'orders/order_detail.html', context)
