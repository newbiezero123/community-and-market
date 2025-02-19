# shop/models.py
from django.db import models
from django.contrib.auth.models import User

# Choices สำหรับ category และ size
CATEGORY_CHOICES = [
    ('general', 'ทั่วไป'),
    ('clothing', 'เสื้อผ้า'),
    ('electronics', 'อุปกรณ์อิเล็กทรอนิกส์'),
    ('books', 'หนังสือ'),
]

SIZE_CHOICES = [
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

class Product(models.Model):
    name = models.CharField(max_length=255)  # ชื่อสินค้า
    description = models.TextField()  # รายละเอียด
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ราคา
    stock = models.PositiveIntegerField()  # จำนวนสินค้า
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # รูปสินค้า
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')  # ประเภทสินค้า

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('store', 'รับที่คณะ'),
        ('home', 'จัดส่งถึงบ้าน'),
    ]
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('shipped', 'กำลังจัดส่ง'),
        ('completed', 'เสร็จสมบูรณ์'),
        ('cancelled', 'ยกเลิก'),
        ('pickup', 'สินค้าพร้อมรับ'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ใช้ user เป็น FK
    created_at = models.DateTimeField(auto_now_add=True)  # วันที่สร้างคำสั่งซื้อ
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # ราคารวม
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # สถานะการดำเนินการ
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='store')  # วิธีจัดส่ง
    shipping_address = models.TextField(blank=True, null=True)  # ที่อยู่จัดส่ง
    payment_slip = models.ImageField(upload_to='payment_slips/', null=True, blank=True)  # สลีปการชำระเงิน
    tracking_number = models.CharField(max_length=100, blank=True, null=True, default='')  # เลขติดตามพัสดุ
    cancellation_reason = models.TextField(blank=True, null=True, default='')  # เหตุผลยกเลิกคำสั่งซื้อ
    buyer_message = models.TextField(blank=True, null=True, verbose_name="ข้อความถึงผู้ขาย")  # ข้อความถึงผู้ขาย

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, blank=True, null=True, verbose_name="Size")  # สำหรับสินค้าเสื้อผ้า

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')  # ผูกกับ User หนึ่งคน
    created_at = models.DateTimeField(auto_now_add=True)  # วันที่สร้างตะกร้า

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=4, choices=SIZE_CHOICES, blank=True, null=True, verbose_name="Size")  # เพิ่มฟิลด์ size สำหรับสินค้าเสื้อผ้าในตะกร้า

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        return self.product.price * self.quantity
