# shop/forms.py
from django import forms 
from .models import Product, Order, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']
        labels = {
            'name': 'ชื่อสินค้า',
            'description': 'รายละเอียด',
            'price': 'ราคา',
            'stock': 'จำนวนสินค้า',
            'image': 'รูปสินค้า',
            'category': 'ประเภทสินค้า'
        }

class OrderForm(forms.ModelForm):
    payment_slip = forms.FileField(required=True, label="อัพโหลดสลิปการชำระเงิน")
    buyer_message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="ข้อความถึงผู้ขาย"
    )
    class Meta:
        model = Order
        fields = ['delivery_method', 'payment_slip', 'buyer_message']
        widgets = {
            'delivery_method': forms.RadioSelect
        }
        labels = {
            'delivery_method': 'วิธีการรับสินค้า',
            'payment_slip': 'อัพโหลดสลิปการชำระเงิน'
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'size']
        labels = {
            'quantity': 'จำนวน',
            'size': 'ขนาด'
        }
