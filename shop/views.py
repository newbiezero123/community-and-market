# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect 
from .models import Order, OrderItem, Product, Cart, CartItem
from .forms import ProductForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import Address
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from collections import defaultdict
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.utils import timezone


def product_list(request):
    products = Product.objects.all()  # ดึงสินค้าทั้งหมดจากฐานข้อมูล
    return render(request, 'shop/product_list.html', {'products': products})

def add_product(request):
    if not request.user.is_superuser:
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/add_product.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def purchase_item(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    user_address = None
    try:
        user_address = request.user.address
    except Address.DoesNotExist:
        user_address = None

    quantity = 1
    total_price = product.price
    delivery_fee = 50

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        delivery_method = request.POST.get('delivery_method')
        if form.is_valid():
            if product.stock < 1:
                messages.error(request, f"ขออภัย สินค้า {product.name} หมดสต็อก")
                return redirect('shop:product_detail', product_id=product.id)
            if delivery_method == 'home':
                total_price += delivery_fee
                if not user_address:
                    messages.error(request, "กรุณาเพิ่มที่อยู่ก่อนสั่งซื้อแบบจัดส่งถึงบ้าน")
                    return redirect('accounts:add_address')
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            if delivery_method == 'home' and user_address:
                order.shipping_address = f"{user_address.name}, {user_address.street}, {user_address.city}, {user_address.state}, {user_address.zip_code}, {user_address.country}, {user_address.phone}"
            else:
                order.shipping_address = f"รับที่คณะ โทร {user_address.phone if user_address else ''}"
            order.save()
            product.stock -= 1
            product.save()
            size = None
            if product.category == 'clothing':
                size = request.POST.get('size')
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=1,
                price=product.price,
                size=size
            )
            order_item.save()
            messages.success(request, "คำสั่งซื้อถูกสร้างเรียบร้อยแล้ว!")
            return redirect('product_list')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'product': product,
        'user_address': user_address,
        'total_price': total_price,
        'delivery_fee': delivery_fee,
        'quantity': quantity,
        'show_size': product.category == 'clothing',  # flag สำหรับแสดงตัวเลือก size ในเทมเพลต
    }
    return render(request, 'shop/purchase_item.html', context)

@login_required
def purchase_cart_items(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, "ตะกร้าของคุณว่างเปล่า กรุณาเลือกสินค้าก่อนสั่งซื้อ")
        return redirect('shop:product_list')
    total_price = cart.total_price()
    delivery_fee = 50
    user_address = None
    total_price_with_delivery = total_price
    try:
        user_address = request.user.address
    except Address.DoesNotExist:
        user_address = None

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        delivery_method = request.POST.get('delivery_method')
        if form.is_valid():
            if delivery_method == 'home':
                total_price += delivery_fee
                if not user_address:
                    messages.error(request, "กรุณาเพิ่มที่อยู่ก่อนสั่งซื้อแบบจัดส่งถึงบ้าน")
                    return redirect('accounts:add_address')
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            if delivery_method == 'home' and user_address:
                order.shipping_address = f"{user_address.name}, {user_address.street}, {user_address.city}, {user_address.state}, {user_address.zip_code}, {user_address.country}, {user_address.phone}"
            else:
                order.shipping_address = 'รับที่คณะ'
            order.save()
            # สำหรับแต่ละรายการในตะกร้า หากสินค้าเป็นเสื้อผ้า ให้คัดลอกค่า size จาก CartItem
            for cart_item in cart.items.all():
                order_item = OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    size=cart_item.size
                )
                order_item.save()
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            cart.items.all().delete()
            messages.success(request, "คำสั่งซื้อของคุณถูกสร้างเรียบร้อยแล้ว!")
            return redirect('product_list')
    else:
        form = OrderForm()
    return render(request, 'shop/purchase_cart_items.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
        'delivery_fee': delivery_fee,
        'user_address': user_address,
        'total_price_with_delivery': total_price_with_delivery,
    })


@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'เพิ่ม {product.name} เข้าตะกร้าแล้ว!')
    return redirect('product_list')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        # รับค่า quantity และ size (ถ้ามี)
        quantity = int(request.POST.get('quantity', cart_item.quantity))
        size = request.POST.get('size')
        
        if quantity > cart_item.product.stock:
            quantity = cart_item.product.stock
            messages.warning(request, f"สินค้า {cart_item.product.name} มีจำนวนในสต็อกเพียง {cart_item.product.stock} ชิ้น ระบบได้ปรับให้เป็นจำนวนสูงสุดแล้ว")
        
        if quantity > 0:
            cart_item.quantity = quantity
            # หากสินค้าเป็นเสื้อผ้า ให้บันทึกค่า size
            if cart_item.product.category == 'clothing':
                cart_item.size = size
            cart_item.save()
            messages.success(request, f"อัปเดตจำนวน {cart_item.product.name} เรียบร้อย")
        else:
            cart_item.delete()
            messages.success(request, f"ลบสินค้า {cart_item.product.name} ออกจากตะกร้าแล้ว")
    
    return redirect('view_cart')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def order_history_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        if 'mark_completed' in request.POST:
            if order.status in ['shipped', 'pickup']:
                order.status = 'completed'
                order.save()
            return redirect('order_history_detail', order_id=order.id)
    return render(request, 'shop/order_history_detail.html', {'order': order})

@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'shipped':
            order.status = 'shipped'
            order.tracking_number = request.POST.get('tracking_number')
        elif status == 'pickup':  
            order.status = 'pickup'
        elif status == 'cancelled':
            order.status = 'cancelled'
            order.cancellation_reason = request.POST.get('cancellation_reason')
        elif status == 'completed':
            order.status = 'completed'
        order.save()
        return redirect('order_detail', order_id=order.id)
    return render(request, 'shop/order_detail.html', {'order': order})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"อัปเดตสถานะคำสั่งซื้อ #{order.id} เป็น {order.get_status_display()} เรียบร้อยแล้ว")
        else:
            messages.error(request, "สถานะไม่ถูกต้อง")
    return HttpResponseRedirect(reverse('order_list'))

@staff_member_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'shop/manage_products.html', {'products': products})

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "อัปเดตสินค้าสำเร็จ!")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "ลบสินค้าสำเร็จ!")
    return redirect('manage_products')

@staff_member_required
def sales_report(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    seven_days_ago = today - timedelta(days=6)

    # คำนวณยอดขายวันนี้
    sales_today = OrderItem.objects.filter(
        order__created_at__date=today
    ).aggregate(
        total_sales=Sum(
            ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        )
    )['total_sales'] or 0

    # คำนวณยอดขาย 7 วันล่าสุด (รวมวันนี้ด้วย)
    sales_last_7_dayssum = OrderItem.objects.filter(
        order__created_at__date__range=(seven_days_ago, today)
    ).aggregate(
        total_sales=Sum(
            ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        )
    )['total_sales'] or 0

    # คำนวณยอดขายเดือนนี้
    sales_this_month = OrderItem.objects.filter(
        order__created_at__date__gte=start_of_month
    ).aggregate(
        total_sales=Sum(
            ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        )
    )['total_sales'] or 0

    sales_last_7_days = defaultdict(list)
    sales_data = OrderItem.objects.filter(order__created_at__date__gte=seven_days_ago) \
        .values('order__created_at__date', 'product__name', 'price') \
        .annotate(
            total_sales=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())),
            total_quantity=Sum('quantity')
        ).order_by('-order__created_at__date')
    
    for sale in sales_data:
        # คำนวณราคาต่อชิ้น (price per unit) โดยใช้ price เดิมจาก OrderItem
        price_per_unit = sale['price']
        
        sales_last_7_days[sale['order__created_at__date']].append({
            'product_name': sale['product__name'],
            'total_sales': sale['total_sales'],
            'total_quantity': sale['total_quantity'],
            'price_per_unit': price_per_unit  # เพิ่มราคาต่อชิ้น
        })
    
    return render(request, 'shop/sales_report.html', {
        'sales_today': sales_today,
        'sales_last_7_dayssum': sales_last_7_dayssum,
        'sales_this_month': sales_this_month,
        'sales_last_7_days': dict(sales_last_7_days),
    })
