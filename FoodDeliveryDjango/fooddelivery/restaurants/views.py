from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Restaurant, Category, MenuItem

def restaurant_list(request):
    """Display a list of all restaurants, with optional search functionality."""
    query = request.GET.get('q', '')
    
    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) | 
            Q(cuisine_type__icontains=query) |
            Q(description__icontains=query)
        ).order_by('name')
    else:
        restaurants = Restaurant.objects.all().order_by('name')
    
    context = {
        'restaurants': restaurants,
        'query': query
    }
    
    return render(request, 'restaurants/list.html', context)

def restaurant_detail(request, restaurant_id):
    """Display details of a specific restaurant and its menu."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    categories = Category.objects.filter(restaurant=restaurant)
    
    # Get menu items organized by category
    menu_by_category = {}
    for category in categories:
        menu_by_category[category] = MenuItem.objects.filter(
            category=category, 
            is_available=True
        ).order_by('name')
    
    context = {
        'restaurant': restaurant,
        'menu_by_category': menu_by_category
    }
    
    return render(request, 'restaurants/detail.html', context)
