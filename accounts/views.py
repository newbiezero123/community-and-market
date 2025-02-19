from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.views import LogoutView
from .forms import AddressForm
from .models import Address
from django.contrib.admin.views.decorators import staff_member_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # update_or_create จะอัปเดตข้อมูลหากมี UserProfile อยู่แล้ว
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'major': form.cleaned_data.get('major', ''),
                    'phone_number': form.cleaned_data.get('phone_number', '')
                }
            )
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    # ดึงข้อมูลที่อยู่ที่เกี่ยวข้องกับ user ปัจจุบัน
    address = Address.objects.filter(user=request.user).first()

    return render(request, 'registration/profile.html', {
        'address': address
    })

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def manage_address(request):
    try:
        address = request.user.address  # ดึงที่อยู่ของผู้ใช้
    except Address.DoesNotExist:
        address = None

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')  # ส่งกลับไปที่หน้าโปรไฟล์
    else:
        form = AddressForm(instance=address)

    return render(request, 'registration/manage_address.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')