from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """Modelo de Categoría para clasificar los posts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Genera automáticamente el slug a partir del nombre."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    """Modelo de Post/Artículo del blog."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Genera automáticamente el slug a partir del título."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Modelo de Comentario en un post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Comentarios"
        ordering = ['created_at']

    def __str__(self):
        return f"Comentario de {self.author.username} en {self.post.title}"


class Profile(models.Model):
    """Modelo de Perfil de Usuario con roles."""
    ROLE_CHOICES = [
        ('visitante', 'Visitante'),
        ('miembro', 'Miembro'),
        ('colaborador', 'Colaborador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='miembro')

    class Meta:
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"Perfil de {self.user.username} - {self.get_role_display()}"

    def get_role_display(self):
        return dict(self.ROLE_CHOICES)[self.role]

    def is_collaborator(self):
        """Retorna True si el usuario es colaborador o superusuario."""
        return self.role == 'colaborador' or self.user.is_superuser

    def is_member(self):
        """Retorna True si el usuario es miembro o superior."""
        return self.role in ['miembro', 'colaborador'] or self.user.is_superuser
