from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import PostForm

def post_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    posts = Post.objects.all()
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if category:
        posts = posts.filter(category__slug=category)
    
    paginator = Paginator(posts, 10)  # 10 โพสต์ต่อหน้า
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'posts/post_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'โพสต์ถูกสร้างเรียบร้อยแล้ว')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # เพิ่ม view count
    post.view_count += 1
    post.save()
    
    # ดึงคอมเม้นทั้งหมดของโพสต์ (เรียงจากล่าสุดไปเก่าสุด)
    comments = post.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'กรุณาเข้าสู่ระบบก่อนที่จะส่งคอมเม้น')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'คอมเม้นของคุณถูกเพิ่มแล้ว')
            # Redirect กลับไปที่หน้า post_detail เพื่อแสดงคอมเม้นใหม่
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'posts/post_detail.html', context)


def home(request):
    # ดึงโพสต์ 3 รายการล่าสุดจากฐานข้อมูล
    latest_posts = Post.objects.all().order_by('-created_at')[:3]  # จำกัดแค่ 3 โพสต์ล่าสุด
    return render(request, 'home.html', {'latest_posts': latest_posts})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # ตรวจสอบว่าเป็นเจ้าของโพสต์หรือ superuser
    if post.author == request.user or request.user.is_superuser:
        post.delete()
        return redirect('post_list')  # หลังจากลบเสร็จจะ redirect ไปหน้าโพสต์ทั้งหมด
    else:
        return redirect('post_list')  # ถ้าไม่ใช่เจ้าของโพสต์ หรือ superuser ก็จะไม่ทำการลบ

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # ตรวจสอบว่าเป็นเจ้าของคอมเมนต์หรือ superuser
    if comment.author == request.user or request.user.is_superuser:
        comment.delete()
    
    # หลังจากลบคอมเมนต์แล้วให้กลับไปที่โพสต์เดิม
    return redirect('post_detail', post_id=comment.post.id)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # ตรวจสอบสิทธิ์การแก้ไขโพสต์: ให้แก้ไขได้เฉพาะเจ้าของโพสต์หรือ superuser
    if not (request.user == post.author or request.user.is_superuser):
        messages.error(request, "คุณไม่มีสิทธิ์แก้ไขโพสต์นี้")
        return redirect(post.get_absolute_url())
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "โพสต์ของคุณถูกแก้ไขแล้ว")
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})