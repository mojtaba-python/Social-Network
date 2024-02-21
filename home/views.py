from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment, Like
from .forms import PostUpdateForm, PostCreateForm, CommentCreateForm, ReplayCommentForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        post = Post.objects.all()
        if request.GET.get('search'):
            post = post.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'post': post, 'form_search':self.form_class})


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = ReplayCommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomment.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/detail.html', {'post':self.post_instance, 'comment':comment,
         'form':self.form_class, 'form_reply':self.form_class_reply, 'can_like':can_like})

    @method_decorator(login_required)
    def post(self, request, post_id, post_slug):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.post_instance
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'successs')
            return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)
            

class PostDeleteView(LoginRequiredMixin, View):
    def get(self,request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted success', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('home:home')
        

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form':form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.image = request.FILES['image']
            new_post.save()
            messages.success(request, 'you updated this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)
             

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm
   
    def get(self, request):
        form = self.form_class()
        return render(request, 'home/create.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.image = request.FILES['image']
            new_post.save()
            messages.success(request, 'you created a new post', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


class ReplayCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id):
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.get(pk=comment_id)
        form = ReplayCommentForm(request.POST)
        if form.is_valid():
            reply_comment = form.save(commit=False)
            reply_comment.user = request.user
            reply_comment.post = post
            reply_comment.reply = comment
            reply_comment.is_reply = True
            reply_comment.save()
            messages.success(request, 'your send reply comment successfully', 'success')
        return redirect('home:post_detail', post.id, post.slug)

    
class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            messages.error(request, 'you after liken this post!', 'warning')
        else:
            Like.objects.create(user=request.user, post=post)
            messages.success(request, 'you liked this post successfully', 'success')
        return redirect('home:post_detail', post.id, post.slug)

