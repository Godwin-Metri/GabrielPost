from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogModel, CommentModel, AddBlogModel
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import AddBlogContentForm
from django.contrib.auth.models import User


class HomePage(ListView):
    model = BlogModel
    template_name = 'blog/home.html'
    ordering = [
        '-date_posted_on'
    ]
    context_object_name = 'blogs'


@login_required()
def blogDetail(request, slug):
    user = User.objects.get(id=request.user.id)

    post_all = BlogModel.objects.all()[:5]
    post = BlogModel.objects.filter(slug=slug).first()
    if not post:
        return render(request, 'blog/pageNotFound.html', context=None)
    additional_content = AddBlogModel.objects.filter(blog=post)
    if request.method == 'POST':
        comment_object = CommentModel(blog=post, comment_author=request.user, comment=request.POST['commentText'])
        comment_object.save()
        return redirect(f'/blog/{slug}/')

    if post in user.post_likes.all():
        has_liked = True
    else:
        has_liked = False

    context = {
        'blog': post,
        'username': request.user,
        'all_post': post_all,
        'additional_content': additional_content,
        'has_liked': has_liked,
    }
    return render(request, 'blog/blogDetail.html', context=context)


class CreateBlogView(CreateView):
    model = BlogModel
    fields = ['blog_title', 'blog_short_desc', 'blog_image', 'blog_complete_desc', 'blog_language',]
    template_name = 'blog/createBlog.html'

    def form_valid(self, form):
        form.instance.blog_author = self.request.user
        return super().form_valid(form)


class UpdateBlogView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogModel
    fields = ['blog_title', 'blog_short_desc','blog_image','blog_complete_desc','blog_language']
    template_name = 'blog/updateBlog.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.blog_author == self.request.user:
            return True
        return False


class DeleteBlogView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogModel
    template_name = 'blog/postDelete.html'
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if post.blog_author == self.request.user:
            return True
        return False


# class AddContentView(CreateView):
#     template_name = 'blog/addcontent.html'
#     model = AddBlogModel
#     fields = ['title', 'image', 'body']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.blog = self.kwargs.get('id')
#         return super().form_valid(form)


def addContent(request, slug):
    post = BlogModel.objects.filter(slug=slug)

    if request.method == 'POST':
        content = AddBlogContentForm(request.POST, request.FILES)
        if content.is_valid():
            content.instance.author = request.user
            content.instance.blog = post.first()
            content.save()
            return redirect(f'/blog/{slug}')
    else:
        content = AddBlogContentForm()
    return render(request, 'blog/addcontent.html', context={'form': content})


@login_required()
def like(request, slug):
    blog = BlogModel.objects.filter(slug=slug)
    if not blog:
        return redirect(request, 'blog/pageNotFound.html', context=None)
    else:
        blog = blog.first()
    if request.method == 'POST':
        blog.likes.add(request.user)
        return redirect(blog.get_absolute_url())


@login_required()
def dislike(request, slug):
    blog = BlogModel.objects.filter(slug=slug)
    if not blog:
        return redirect(request, 'blog/pageNotFound.html', context=None)
    else:
        blog = blog.first()
    if request.method == 'POST':
        blog.likes.remove(request.user)
        return redirect(blog.get_absolute_url())
