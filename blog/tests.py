from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Category, Post, Comment, Profile


class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""

    def setUp(self):
        self.category = Category.objects.create(name="Nutrición")

    def test_category_creation(self):
        """Verifica que se crea una categoría correctamente"""
        self.assertEqual(self.category.name, "Nutrición")
        self.assertEqual(str(self.category), "Nutrición")

    def test_slug_generation(self):
        """Verifica que el slug se genera automáticamente"""
        self.assertEqual(self.category.slug, "nutricion")

    def test_category_unique_name(self):
        """Verifica que el nombre de categoría es único"""
        with self.assertRaises(Exception):
            Category.objects.create(name="Nutrición")


class PostModelTest(TestCase):
    """Tests para el modelo Post"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Fitness")
        self.post = Post.objects.create(
            title="Mi primer post",
            category=self.category,
            author=self.user,
            content="Contenido del post",
        )

    def test_post_creation(self):
        """Verifica que se crea un post correctamente"""
        self.assertEqual(self.post.title, "Mi primer post")
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.is_published)

    def test_slug_generation(self):
        """Verifica que el slug se genera automáticamente"""
        self.assertEqual(self.post.slug, "mi-primer-post")

    def test_slug_uniqueness(self):
        """Verifica que los slugs duplicados se manejan correctamente"""
        post2 = Post.objects.create(
            title="Mi primer post",  # Mismo título
            category=self.category,
            author=self.user,
            content="Otro contenido",
        )
        self.assertNotEqual(self.post.slug, post2.slug)
        self.assertEqual(post2.slug, "mi-primer-post-1")

    def test_post_get_absolute_url(self):
        """Verifica que get_absolute_url devuelve la URL correcta"""
        url = self.post.get_absolute_url()
        self.assertEqual(url, reverse("blog:post_detail", kwargs={"slug": self.post.slug}))


class CommentModelTest(TestCase):
    """Tests para el modelo Comment"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Salud")
        self.post = Post.objects.create(
            title="Post de prueba",
            category=self.category,
            author=self.user,
            content="Contenido",
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Excelente post!",
        )

    def test_comment_creation(self):
        """Verifica que se crea un comentario correctamente"""
        self.assertEqual(self.comment.content, "Excelente post!")
        self.assertEqual(self.comment.author, self.user)
        self.assertTrue(self.comment.is_active)

    def test_comment_str(self):
        """Verifica la representación en string del comentario"""
        expected_str = f"Comentario de {self.user.username} en {self.post.title}"
        self.assertEqual(str(self.comment), expected_str)


class ProfileModelTest(TestCase):
    """Tests para el modelo Profile"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_profile_auto_creation(self):
        """Verifica que se crea un Profile automáticamente al crear un User"""
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertEqual(self.user.profile.role, "visitante")

    def test_is_collaborator(self):
        """Verifica el método is_collaborator()"""
        self.assertFalse(self.user.profile.is_collaborator())
        self.user.profile.role = "colaborador"
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_collaborator())

    def test_is_member(self):
        """Verifica el método is_member()"""
        self.assertFalse(self.user.profile.is_member())
        self.user.profile.role = "miembro"
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_member())


class HomeViewTest(TestCase):
    """Tests para la vista home"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Fitness")
        self.post = Post.objects.create(
            title="Post público",
            category=self.category,
            author=self.user,
            content="Contenido público",
            is_published=True,
        )

    def test_home_view_status_code(self):
        """Verifica que la vista home retorna status 200"""
        response = self.client.get(reverse("blog:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Verifica que usa el template correcto"""
        response = self.client.get(reverse("blog:home"))
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_home_shows_published_posts(self):
        """Verifica que solo muestra posts publicados"""
        response = self.client.get(reverse("blog:home"))
        self.assertContains(response, self.post.title)

    def test_home_pagination(self):
        """Verifica que la paginación funciona"""
        # Crear 6 posts para forzar paginación (5 por página)
        for i in range(5):
            Post.objects.create(
                title=f"Post {i}",
                category=self.category,
                author=self.user,
                content="Contenido",
                is_published=True,
            )
        response = self.client.get(reverse("blog:home"))
        self.assertTrue(response.context["is_paginated"])


class PostDetailViewTest(TestCase):
    """Tests para la vista de detalle de post"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Salud")
        self.post = Post.objects.create(
            title="Post detalle",
            category=self.category,
            author=self.user,
            content="Contenido del post",
            is_published=True,
        )

    def test_post_detail_view_status_code(self):
        """Verifica que retorna status 200"""
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template(self):
        """Verifica que usa el template correcto"""
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_post_detail_contains_post_content(self):
        """Verifica que muestra el contenido del post"""
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)


class PostCreateViewTest(TestCase):
    """Tests para crear posts"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="collaborator", password="testpass123"
        )
        self.user.profile.role = "colaborador"
        self.user.profile.save()
        self.category = Category.objects.create(name="Fitness")

    def test_create_post_requires_login(self):
        """Verifica que solo usuarios autenticados pueden crear posts"""
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 302)  # Redirección a login

    def test_create_post_requires_collaborator_role(self):
        """Verifica que solo colaboradores pueden crear posts"""
        self.client.login(username="collaborator", password="testpass123")
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_post_successfully(self):
        """Verifica que se crea un post correctamente"""
        self.client.login(username="collaborator", password="testpass123")
        data = {
            "title": "Nuevo post",
            "category": self.category.id,
            "content": "Contenido del nuevo post",
            "is_published": True,
        }
        response = self.client.post(reverse("blog:post_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirección tras crear
        self.assertTrue(Post.objects.filter(title="Nuevo post").exists())

    def test_create_post_non_collaborator_forbidden(self):
        """Verifica que visitantes no pueden crear posts"""
        user = User.objects.create_user(username="visitante", password="testpass123")
        self.client.login(username="visitante", password="testpass123")
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 403)  # Forbidden


class PostUpdateViewTest(TestCase):
    """Tests para editar posts"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="author", password="testpass123"
        )
        self.user.profile.role = "colaborador"
        self.user.profile.save()
        self.category = Category.objects.create(name="Salud")
        self.post = Post.objects.create(
            title="Post original",
            category=self.category,
            author=self.user,
            content="Contenido original",
        )

    def test_update_post_by_author(self):
        """Verifica que el autor puede editar su propio post"""
        self.client.login(username="author", password="testpass123")
        data = {
            "title": "Post actualizado",
            "category": self.category.id,
            "content": "Contenido actualizado",
            "is_published": True,
        }
        response = self.client.post(
            reverse("blog:post_update", kwargs={"slug": self.post.slug}), data
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Post actualizado")

    def test_update_post_by_other_user_forbidden(self):
        """Verifica que otros usuarios no pueden editar posts"""
        other_user = User.objects.create_user(
            username="other", password="testpass123"
        )
        other_user.profile.role = "colaborador"
        other_user.profile.save()
        self.client.login(username="other", password="testpass123")
        response = self.client.get(
            reverse("blog:post_update", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden


class PostDeleteViewTest(TestCase):
    """Tests para eliminar posts"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="author", password="testpass123"
        )
        self.user.profile.role = "colaborador"
        self.user.profile.save()
        self.category = Category.objects.create(name="Bienestar")
        self.post = Post.objects.create(
            title="Post a eliminar",
            category=self.category,
            author=self.user,
            content="Contenido",
        )

    def test_delete_post_by_author(self):
        """Verifica que el autor puede eliminar su propio post"""
        self.client.login(username="author", password="testpass123")
        response = self.client.post(
            reverse("blog:post_delete", kwargs={"slug": self.post.slug})
        )
        self.assertFalse(Post.objects.filter(slug=self.post.slug).exists())

    def test_delete_post_by_other_user_forbidden(self):
        """Verifica que otros usuarios no pueden eliminar posts"""
        other_user = User.objects.create_user(
            username="other", password="testpass123"
        )
        other_user.profile.role = "colaborador"
        other_user.profile.save()
        self.client.login(username="other", password="testpass123")
        response = self.client.get(
            reverse("blog:post_delete", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden


class CommentCRUDTest(TestCase):
    """Tests para comentarios"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="user1", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="user2", password="testpass123"
        )
        self.category = Category.objects.create(name="Fitness")
        self.post = Post.objects.create(
            title="Post comentable",
            category=self.category,
            author=self.user,
            content="Contenido",
            is_published=True,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Mi comentario",
        )

    def test_edit_own_comment(self):
        """Verifica que un usuario puede editar su propio comentario"""
        self.client.login(username="user1", password="testpass123")
        data = {"content": "Comentario editado"}
        response = self.client.post(
            reverse("blog:comment_edit", kwargs={"pk": self.comment.pk}), data
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Comentario editado")

    def test_delete_own_comment(self):
        """Verifica que un usuario puede eliminar su propio comentario"""
        self.client.login(username="user1", password="testpass123")
        response = self.client.post(
            reverse("blog:comment_delete", kwargs={"pk": self.comment.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_edit_other_comment_forbidden(self):
        """Verifica que no se puede editar comentario de otro usuario"""
        self.client.login(username="user2", password="testpass123")
        response = self.client.get(
            reverse("blog:comment_edit", kwargs={"pk": self.comment.pk})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden


class SignupViewTest(TestCase):
    """Tests para registro de usuarios"""

    def setUp(self):
        self.client = Client()

    def test_signup_view_status_code(self):
        """Verifica que la vista signup retorna status 200"""
        response = self.client.get(reverse("blog:signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_creates_user(self):
        """Verifica que se crea un usuario correctamente"""
        data = {
            "username": "newuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        response = self.client.post(reverse("blog:signup"), data)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_creates_profile(self):
        """Verifica que se crea un Profile automáticamente"""
        data = {
            "username": "newuser",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        }
        response = self.client.post(reverse("blog:signup"), data)
        user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(user.profile.role, "visitante")


class CategoryFilteringTest(TestCase):
    """Tests para filtrado por categoría"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.cat1 = Category.objects.create(name="Nutrición")
        self.cat2 = Category.objects.create(name="Ejercicio")
        self.post1 = Post.objects.create(
            title="Post nutrición",
            category=self.cat1,
            author=self.user,
            content="Sobre nutrición",
            is_published=True,
        )
        self.post2 = Post.objects.create(
            title="Post ejercicio",
            category=self.cat2,
            author=self.user,
            content="Sobre ejercicio",
            is_published=True,
        )

    def test_category_filter_works(self):
        """Verifica que el filtro por categoría funciona"""
        response = self.client.get(
            reverse("blog:category_posts", kwargs={"slug": self.cat1.slug})
        )
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)
