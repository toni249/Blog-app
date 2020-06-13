from .models import Post
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileUpdateForm,UserRegisterForm,NewPostForm
from django.views.generic import (       
                ListView, 
                DetailView,
                CreateView,
                UpdateView,
                DeleteView
            )

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog_post.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = 'user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html' 


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html' 

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/user/'
    template_name = 'post_delete_form.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f' Your account has been created !')
			return redirect('user-login')
	else :
		form = UserRegisterForm()
	return render(request,'user/user_register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)




# def about(request):
#     return render(request, 'blog/about.html', {'title': 'About'})