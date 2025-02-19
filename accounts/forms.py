from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Address

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    major = forms.ChoiceField(  # เปลี่ยนจาก CharField เป็น ChoiceField
        choices=UserProfile.MAJOR_CHOICES, 
        required=False,
        widget=forms.Select(  # เพิ่ม widget เป็น Select เพื่อให้เป็น dropdown
            attrs={'class': 'form-control'}  # เพิ่ม class bootstrap เพื่อให้สวยงาม
        )
    )
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                major=self.cleaned_data.get('major'),
                phone_number=self.cleaned_data.get('phone_number')
            )
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone', 'street', 'city', 'state', 'zip_code', 'country']
        labels = {
            'name': 'ชื่อ-นามสกุล',
            'phone': 'เบอร์ติดต่อ',
            'street': 'ที่อยู่',
            'city': 'อำเภอ/เขต',
            'state': 'จังหวัด',
            'zip_code': 'รหัสไปรษณีย์', 
            'country': 'ประเทศ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }