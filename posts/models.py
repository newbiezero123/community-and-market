# models.py (ในแอป posts)
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # ยังคงใช้ slug สำหรับ Category เพื่อความสะดวกในการจัดการ (เช่น filter)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.summary and self.content:
            self.summary = self.content[:250] + '...'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # เปลี่ยนจาก slug เป็นการใช้ primary key
        return reverse('post_detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
