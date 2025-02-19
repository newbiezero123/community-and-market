from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    # เพิ่ม custom action สำหรับรีเซ็ตรหัสผ่าน
    actions = ['reset_password']
    
    def reset_password(self, request, queryset):
        for user in queryset:
            # เปลี่ยนรหัสผ่านเป็น 'new_password'
            user.set_password('new_password')
            user.save()
        self.message_user(request, "รีเซ็ตรหัสผ่านสำเร็จสำหรับผู้ใช้ที่เลือก")
    reset_password.short_description = "รีเซ็ตรหัสผ่านให้กับผู้ใช้ที่เลือก"

# ลงทะเบียน CustomUserAdmin แทนที่ Default User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)

admin.site.index_title = "Welcome to Ru Comunity Admin" # ข้อความหน้าแรกของ admin