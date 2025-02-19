from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    MAJOR_CHOICES = [
        ('computer', 'วิศวกรรมคอมพิวเตอร์'),
        ('civil', 'วิศวกรรมโยธา'),
        ('industrial', 'วิศวกรรมอุตสาหการ'),
        ('energy', 'วิศวกรรมพลังงาน'),
        ('environment', 'วิศวกรรมสิ่งแวดล้อม'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

class Address(models.Model):
    name = models.CharField(max_length=255, verbose_name="ชื่อ-นามสกุล", null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name="เบอร์ติดต่อ", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length=255, verbose_name="ที่อยู่")
    city = models.CharField(max_length=100, verbose_name="เมือง")
    state = models.CharField(max_length=100, verbose_name="จังหวัด")
    zip_code = models.CharField(max_length=10, verbose_name="รหัสไปรษณีย์")
    country = models.CharField(max_length=100, verbose_name="ประเทศ", default="ประเทศไทย")

    def __str__(self):
        return f"{self.user.username} - {self.street}"
