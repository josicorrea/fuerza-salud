from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView



def home(request):
    """Lista de posts con paginación, filtro por categoría y orden."""
    qs = Post.objects.filter(is_published=True)

    # filtros
    category_slug = request.GET.get('category')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    order = request.GET.get('order', 'date_desc')
    if order == 'date_asc':
        qs = qs.order_by('created_at')
    elif order == 'title_asc':
        qs = qs.order_by('title')
    elif order == 'title_desc':
        qs = qs.order_by('-title')
    else:  # date_desc por defecto
        qs = qs.order_by('-created_at')

    # paginación
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    paginator = Paginator(qs, 5)  # 5 posts por página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_slug,
        'current_order': order,
        'paginator': paginator,
        'is_paginated': posts.has_other_pages(),
    }
    return render(request, 'blog/post_list.html', context)


def category_posts(request, slug):
    """Redirige a la lista de posts filtrada por categoría usando la misma lógica que `home`.
    Mantiene los parámetros de orden y paginación desde querystring.
    """
    # simplemente reutilizamos home pasando el parámetro category en GET
    # construimos una QueryDict y re-dispatchamos a home
    request_get = request.GET.copy()
    request_get['category'] = slug
    request.GET = request_get
    return home(request)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = post.comments.filter(is_active=True).order_by('created_at')

    # manejo del envío del formulario de comentario
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para comentar.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Tu comentario fue publicado.')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


class CommentEditMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        comment = self.get_object()
        # autor del comentario puede editar
        if comment.author == user:
            return True
        # autor del post que sea colaborador puede moderar (editar/borrar)
        post_author = comment.post.author
        profile = getattr(post_author, 'profile', None)
        if profile and profile.is_collaborator() and post_author == user:
            return True
        return False


class CommentUpdateView(LoginRequiredMixin, CommentEditMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'


class CommentDeleteView(LoginRequiredMixin, CommentEditMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def signup(request):
    """Vista simple de registro usando UserCreationForm.

    Crea el usuario y lo loguea inmediatamente, luego redirige al home.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class IsCollaboratorMixin(UserPassesTestMixin):
    """Mixin para comprobar si el usuario es colaborador o superuser."""

    def test_func(self):
        user = self.request.user
        # si no está autenticado, deniega
        if not user.is_authenticated:
            return False
        # superusuario permite todo
        if user.is_superuser:
            return True
        # comprobar profile (si no existe, denegar)
        profile = getattr(user, 'profile', None)
        if profile is None:
            return False
        return profile.is_collaborator()


class PostCreateView(LoginRequiredMixin, IsCollaboratorMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        if user.is_superuser:
            return True
        profile = getattr(user, 'profile', None)
        # solo el autor del post que además sea colaborador puede editar
        return profile is not None and profile.is_collaborator() and post.author == user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home')

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        if user.is_superuser:
            return True
        profile = getattr(user, 'profile', None)
        return profile is not None and profile.is_collaborator() and post.author == user