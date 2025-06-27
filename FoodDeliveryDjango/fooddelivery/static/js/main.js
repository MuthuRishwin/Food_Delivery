/**
 * Food Delivery App - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // Handle quantity increment/decrement
    const quantityInputs = document.querySelectorAll('input[type=number][name^="quantity"]');
    quantityInputs.forEach(input => {
        // Ensure quantity is at least 1
        input.addEventListener('change', function() {
            if (this.value < 1) {
                this.value = 1;
            }
        });
    });

    // Fade out alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            });
        }, 5000);
    }

    // Add smooth scrolling to menu categories
    const menuLinks = document.querySelectorAll('a[href^="#category-"]');
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Handle sticky menu navigation (if present)
    const menuNav = document.querySelector('.menu-nav');
    if (menuNav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                menuNav.classList.add('fixed-top', 'bg-white', 'shadow-sm');
                document.body.style.paddingTop = menuNav.offsetHeight + 'px';
            } else {
                menuNav.classList.remove('fixed-top', 'bg-white', 'shadow-sm');
                document.body.style.paddingTop = '0';
            }
        });
    }

    // Add loading indicators to forms
    const forms = document.querySelectorAll('form:not(.no-loader)');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButtons = this.querySelectorAll('button[type="submit"], input[type="submit"]');
            submitButtons.forEach(button => {
                const originalContent = button.innerHTML;
                button.setAttribute('data-original-content', originalContent);
                button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Loading...';
                button.disabled = true;
            });
        });
    });

    // Handle image loading errors
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.svg';
            this.alt = 'Image not available';
        });
    });

    // Initialize date and time pickers if any
    const datetimePickers = document.querySelectorAll('.datetimepicker');
    if (datetimePickers.length > 0 && typeof flatpickr === 'function') {
        flatpickr('.datetimepicker', {
            enableTime: true,
            dateFormat: "Y-m-d H:i"
        });
    }

    // Handle address form validation
    const addressForm = document.getElementById('address-form');
    if (addressForm) {
        addressForm.addEventListener('submit', function(event) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                const errorMsg = document.createElement('div');
                errorMsg.className = 'alert alert-danger mt-3';
                errorMsg.textContent = 'Please fill in all required fields.';
                
                // Remove any existing error messages
                const existingError = this.querySelector('.alert-danger');
                if (existingError) {
                    existingError.remove();
                }
                
                this.prepend(errorMsg);
            }
        });
    }

    // Handle payment method selection
    const paymentMethodSelect = document.getElementById('id_payment_method');
    const creditCardFields = document.getElementById('credit-card-details');
    
    if (paymentMethodSelect && creditCardFields) {
        paymentMethodSelect.addEventListener('change', function() {
            if (this.value === 'credit_card' || this.value === 'debit_card') {
                creditCardFields.classList.remove('d-none');
            } else {
                creditCardFields.classList.add('d-none');
            }
        });
    }
});
