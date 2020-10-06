from django.shortcuts import render
from product.models import *
from django.contrib.auth.decorators import login_required
from product.forms import ProductForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.forms import AddressForm
from chat.models import *


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    if request.user is not None and request.user.get_username() != '':
        context['user'] = request.user
    else:
        context['user'] = None
    return render(request, 'product/index.html', context)


@login_required
def my_products(request):
    products = request.user.product_set.all()
    context = {'products': products, 'user': request.user}
    return render(request, 'product/my_products.html', context)


@login_required
def add_product(request):
    context = {'user': request.user}
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return HttpResponseRedirect(reverse('my_products'))
        context['form'] = form
    return render(request, 'product/add_product.html', context)


@login_required
def edit_product(request, pid):
    context = {'user': request.user}
    product = Product.objects.get(id=pid)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            product.product_permanent = None
            product.save()
            return HttpResponseRedirect(reverse('my_products'))
    else:
        form = ProductForm(instance=product)
    context['form'] = form
    return render(request, 'product/add_product.html', context)


@login_required
def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    return HttpResponseRedirect(reverse('my_products'))


@login_required
def show_cart(request):
    context = {'user': request.user}
    try:
        cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    incarts = cart.incart_set.all()
    context['incarts'] = incarts
    total_price = 0
    for i in incarts:
        total_price += i.product.price * i.quantity
    context['total_price'] = total_price
    return render(request, 'product/cart.html', context)


@login_required
def add_to_cart(request, pid):
    try:
        cart = Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    product = Product.objects.get(id=pid)
    if product in cart.products.all():
        incart = InCart.objects.get(cart_id=cart.id, product_id=product.id)
        if product.stock > incart.quantity:
            incart.quantity += 1
            incart.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        if product.stock > 0:
            incart = InCart.objects.create(cart=cart, product=product, quantity=1)
            return HttpResponseRedirect(reverse('index'))
    # product is out of stock
    context = {'user': request.user, 'out_of_stock': True, 'products': Product.objects.all()}
    return render(request, 'product/index.html', context)


@login_required
def delete_from_cart(request, pid):
    cart = Cart.objects.get(user_id=request.user.id)
    product = Product.objects.get(id=pid)
    cart.products.remove(product)
    return HttpResponseRedirect(reverse('cart'))


@login_required
def order_history(request):
    context = {'user': request.user}
    orders = request.user.order_set.all()
    context['orders'] = orders
    return render(request, 'product/order_history.html', context)


@login_required
def order_detail(request, oid):
    context = {'user': request.user}
    order = Order.objects.get(id=oid)
    context['order'] = order
    inorders = order.inorder_set.all()
    context['inorders'] = inorders
    return render(request, 'product/order_detail.html', context)


@login_required
def check_out(request):
    context = {'user': request.user}
    cart = Cart.objects.get(user_id=request.user.id)
    incarts = cart.incart_set.all()
    total_price = 0
    for i in incarts:
        total_price += i.product.price * i.quantity
    context['incarts'] = incarts
    context['total_price'] = total_price
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            order = Order.objects.create(user=request.user, status='C', address=address, total_price=total_price)
            for p in cart.products.all():
                if p.product_permanent is None:
                    p.product_permanent = ProductPermanent.objects.create(name=p.name,
                                                                          price=p.price,
                                                                          description=p.description,
                                                                          seller=p.seller,
                                                                          image=p.image)
                    p.save()
                incart = cart.incart_set.get(product_id=p.id)
                order.products.add(p.product_permanent, through_defaults={'quantity': incart.quantity})
                p.stock -= incart.quantity
                p.save()
            cart.products.clear()
            return HttpResponseRedirect(reverse('order_detail', args=[order.id]))
    else:
        form = AddressForm()
    context['form'] = form
    return render(request, 'product/check_out.html', context)


@login_required
def contact_seller(request, uid):
    seller = User.objects.get(id=uid)
    my_rooms_ids = request.user.chatroom_set.values_list('pk', flat=True)
    try:
        room = seller.chatroom_set.get(pk__in=list(my_rooms_ids))
    except ChatRoom.DoesNotExist:
        room = ChatRoom.objects.create(chat_log='')
        room.members.add(request.user, through_defaults={'name': seller.username})
        room.members.add(seller, through_defaults={'name': request.user.username})
    return HttpResponseRedirect(reverse('chat_room', args=[room.id]))
