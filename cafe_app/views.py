from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import * #Category, MenuItem, Reservation, Order, OrderItem
from .forms import * #ReservationForm, FeedbackForm, OrderForm
import json

def home(request):
    categories = Category.objects.all()[:4]  
    special_items = MenuItem.objects.filter(is_special=True, is_available=True)[:4]  
    return render(request, 'index.html', {
        'categories': categories,
        'special_items': special_items
    })

def menu(request):
    categories = Category.objects.all()
    return render(request, 'menu.html', {'categories': categories})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your reservation has been confirmed. We look forward to serving you!')
            return redirect('reservation')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback! We appreciate your opinion.')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

# def order(request):
#     cart_items = []
#     cart_total = 0
    
#     if 'cart' in request.session:
#         cart = request.session['cart']
#         for item_id, quantity in cart.items():
#             menu_item = get_object_or_404(MenuItem, id=int(item_id))
#             total = menu_item.price * quantity
#             cart_items.append({
#                 'id': menu_item.id,
#                 'name': menu_item.name,
#                 'price': float(menu_item.price),
#                 'quantity': quantity,
#                 'total': float(total)
#             })
#             cart_total += total
    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid() and cart_items:
#             order = form.save(commit=False)
#             order.total_amount = cart_total
#             order.save()
            
#             # Create order items
#             for item in cart_items:
#                 menu_item = get_object_or_404(MenuItem, id=item['id'])
#                 OrderItem.objects.create(
#                     order=order,
#                     menu_item=menu_item,
#                     quantity=item['quantity'],
#                     price=menu_item.price
#                 )
            
#             # Clear the cart
#             request.session['cart'] = {}
#             request.session.modified = True
            
#             messages.success(request, f'Your order has been placed successfully. Order #{order.id}')
#             return redirect('home')
#     else:
#         form = OrderForm()
    
#     return render(request, 'order.html', {
#         'form': form,
#         'cart_items': cart_items,
#         'cart_total': cart_total
#     })



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from .models import MenuItem, Order, OrderItem
# from .forms import OrderForm

def order(request):
    cart_items = []
    cart_total = 0

    
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('menu') 

 
    for item_id, quantity in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
        except MenuItem.DoesNotExist:
            messages.error(request, f"Menu item with ID {item_id} not found.")
            continue  

        total = menu_item.price * quantity
        cart_items.append({
            'id': menu_item.id,
            'name': menu_item.name,
            'price': float(menu_item.price),
            'quantity': quantity,
            'total': float(total)
        })
        cart_total += total

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            if not cart_items:
                messages.error(request, "Cannot place an order with an empty cart.")
                return redirect('menu')

            
            order = form.save(commit=False)
            order.total_amount = cart_total
            order.save()

            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=MenuItem.objects.get(id=item['id']),
                    quantity=item['quantity'],
                    price=item['price']
                )

            
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, f'Your order has been placed successfully! Order #{order.id}')
            return redirect('home')  

    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total
    })


# def order(request):
#     cart_items = request.session.get('cart', [])
#     print("Cart session data:", cart_items)  # Debugging output

#     cart_items = [int(item) for item in cart_items if str(item).isdigit()]
    
#     menu_items = MenuItem.objects.filter(id__in=cart_items)
    
#     return render(request, 'order.html', {'menu_items': menu_items})



def add_to_cart(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        
        
        if menu_item_id in cart:
            cart[menu_item_id] += quantity
        else:
            cart[menu_item_id] = quantity
            
        request.session.modified = True
        messages.success(request, 'Item added to cart successfully!')
        
    return redirect('menu')




def remove_from_cart(request, item_id):
    if 'cart' in request.session and str(item_id) in request.session['cart']:
        cart = request.session['cart']
        del cart[str(item_id)]
        request.session.modified = True
        messages.success(request, 'Item removed from cart successfully!')
    
    return redirect('order')


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback')
    else:
        form = FeedbackForm()

    feedbacks = Feedback.objects.all().order_by('-created_at')

    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedbacks})