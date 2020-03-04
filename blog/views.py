from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


class HomeView(TemplateView):
    template_name = 'index.html'

# an easier index, no need for render
class AboutView(TemplateView):
    template_name = 'about.html'


# homepage to contain listofviews
class PostListView(ListView):
    paginate_by = 10
    queryset = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = PostForm
    model = Post
    # success_url = reverse_lazy('post_list')
    success_message = "Your Post has been submitted"
    # success_url = redirect('post_detail', pk=self.pk)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        # obj = form.instance or self.object
        return reverse_lazy("post_detail", kwargs={'pk': self.object.pk})
    
    
class UpdatePostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    success_url = reverse_lazy('post_detail')
    success_message = "Your Post was successfully updated"
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    success_message = "Post has been deleted"


class PostDraftView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    # paginate_by = 10
    login_url = 'login'
    template_name = 'blog/drafts_list.html'
    # model = Post
    queryset = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    
class ProfileView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = 'registration/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(alias=self.request.user)
        return context

##########################################
###########COMMENTS###############
@login_required
def add_comment_to_post(request,pk):
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
        else:
            form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})


@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)


