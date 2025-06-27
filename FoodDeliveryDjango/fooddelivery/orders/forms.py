from django import forms

class CheckoutForm(forms.Form):
    """Form for collecting delivery and payment information during checkout."""
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Delivery Address",
        required=True
    )
    
    contact_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Contact Phone",
        required=True
    )
    
    PAYMENT_CHOICES = (
        ('cash', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    )
    
    payment_method = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=PAYMENT_CHOICES,
        label="Payment Method",
        required=True
    )
    
    delivery_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label="Delivery Instructions (Optional)",
        required=False
    )
    
    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        
        # Basic phone validation - could be improved with more complex regex
        if not phone.replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        
        return phone
