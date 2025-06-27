from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, AddressForm
from .models import Address

def register(request):
    """Register a new user"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            # Automatically log in the user after registration
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """View and update user profile"""
    user_profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    # Get user's addresses
    addresses = Address.objects.filter(user_profile=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'addresses': addresses
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def address_create(request):
    """Add a new address"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_profile = request.user.profile
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('profile')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {'form': form})

@login_required
def address_edit(request, address_id):
    """Edit an existing address"""
    address = Address.objects.get(id=address_id, user_profile=request.user.profile)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/address_form.html', {'form': form, 'address': address})

@login_required
def address_delete(request, address_id):
    """Delete an address"""
    address = Address.objects.get(id=address_id, user_profile=request.user.profile)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})

@login_required
def set_default_address(request, address_id):
    """Set an address as the default"""
    address = Address.objects.get(id=address_id, user_profile=request.user.profile)
    
    # Clear any existing default addresses
    Address.objects.filter(user_profile=request.user.profile, is_default=True).update(is_default=False)
    
    # Set the selected address as default
    address.is_default = True
    address.save()
    
    messages.success(request, 'Default address updated successfully!')
    return redirect('profile')
