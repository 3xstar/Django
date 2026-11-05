from django.test import TestCase
from django.urls import reverse

from .models import Comment, Post


class AddPostViewTests(TestCase):
    def test_valid_post_is_saved_and_redirects(self):
        response = self.client.post(
            reverse("main:add_post"),
            {"title": "Test post", "content": "Post content"},
        )

        self.assertRedirects(response, reverse("main:index"))
        self.assertTrue(Post.objects.filter(title="Test post").exists())

    def test_invalid_post_renders_form_errors(self):
        response = self.client.post(
            reverse("main:add_post"),
            {"title": "", "content": "Post content"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["post_form"].errors)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_details_page_renders_delete_link(self):
        post = Post.objects.create(title="Test post", content="Post content")

        response = self.client.get(
            reverse("main:post_info", kwargs={"post_id": post.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("main:post_delete", kwargs={"post_id": post.id}),
        )

    def test_comment_is_saved_and_shown_only_on_its_post_page(self):
        post = Post.objects.create(title="Test post", content="Post content")
        post_info_url = reverse("main:post_info", kwargs={"post_id": post.id})

        response = self.client.post(
            post_info_url,
            {"author": "Reader", "content": "A persistent comment"},
        )

        self.assertRedirects(response, post_info_url)
        comment = Comment.objects.get(post=post)
        self.assertEqual(comment.author, "Reader")
        self.assertEqual(comment.content, "A persistent comment")

        detail_response = self.client.get(post_info_url)
        self.assertContains(detail_response, "A persistent comment")
        self.assertContains(detail_response, "Reader")

        index_response = self.client.get(reverse("main:index"))
        self.assertNotContains(index_response, "A persistent comment")

    def test_invalid_comment_is_not_saved(self):
        post = Post.objects.create(title="Test post", content="Post content")

        response = self.client.post(
            reverse("main:post_info", kwargs={"post_id": post.id}),
            {"author": "", "content": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["comment_form"].errors)
        self.assertEqual(Comment.objects.count(), 0)
