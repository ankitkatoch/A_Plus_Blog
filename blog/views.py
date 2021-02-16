from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from hitcount.views import HitCountDetailView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import BlogModel, CommentModel
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/accounts/login'
    model = BlogModel
    fields = ['title', 'description', 'blog_image', 'tags']
    success_url = "/list"
    success_message = "Blog has been created successfully"

    def form_valid(self, form):
        obj = form.save(commit=False)
        form.instance.author = self.request.user
        obj.save()
        return super().form_valid(form)


class BlogListView(TagMixin, ListView):
    model = BlogModel
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number_of_blogs"] = BlogModel.objects.all().count()
        context.update({
        'popular_posts': BlogModel.objects.order_by('-hit_count_generic__hits')[:3], })
        return context


class BlogDetailView(HitCountDetailView, DetailView):
    model = BlogModel
    template_name = 'blog/blogmodel_detail.html'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_items"] = self.object.tags.similar_objects()
        return context


class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BlogModel
    fields = ["title", "description", 'blog_image', 'tags']
    success_url = "/list"
    success_message = "Blog has been updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_status = 1
        context["update_status"] = update_status
        return context


class BlogDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BlogModel
    fields = ['title', 'description', 'blog_image', 'tags']
    success_url = reverse_lazy('blog_list')
    success_message = "Blog has been deleted successfully"
    
    def delete(self, request, *args, **kwargs):
        messages.add_message(request, messages.ERROR, "Blog has been deleted successfully")
        return super().delete(request, *args, **kwargs)


class BlogSearchView(ListView):
    model = BlogModel

    def get_queryset(self):
        query = self.request.GET['query']
        return self.model.objects.filter(title__icontains=query)


class TagIndexView(TagMixin, ListView):
    model = BlogModel
    paginate_by = 3
    template_name = 'blog/blogmodel_list.html'

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.kwargs.get('slug'))


class BlogListHomeView(TagMixin, ListView):
    model = BlogModel
    template_name = 'blog/home.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        'popular_posts': BlogModel.objects.order_by('-hit_count_generic__hits')[:3], })
        return context

@login_required
def share_with_friends(request):
    mail_id = request.POST['email']
    message = request.POST['message']
    url_name = request.POST['url_name']
    if not message:
        message = f'I have shared an article with you\n Click on below link\n' + url_name
    else:
        message += f'\n Click on below link\n' + url_name
    send_mail(
        'From'+" "+request.user.username,
        message,
        'Don.The.Django.Developer@gmail.com',
        [mail_id],
        fail_silently=False,
    )
    messages.info(request, "Article has been shared with your friend")
    return redirect('blog_list')




