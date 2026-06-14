import time
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", password="testpass")

    def test_create_note(self):
        note = Note.objects.create(title="测试笔记", content="这是测试内容", owner=self.user)
        self.assertEqual(str(note), "测试笔记")
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)

    def test_content_html(self):
        note = Note.objects.create(title="MD", content="**bold**", owner=self.user)
        self.assertIn("<strong>bold</strong>", note.content_html)

    def test_default_ordering(self):
        n1 = Note.objects.create(title="旧笔记", content="先创建的", owner=self.user)
        time.sleep(0.01)
        n2 = Note.objects.create(title="新笔记", content="后创建的", owner=self.user)
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], n2)


class NoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", password="testpass")
        self.other_user = User.objects.create_user("other", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.note = Note.objects.create(title="测试笔记", content="测试内容", owner=self.user)

    # ---- 列表视图 ----

    def test_list_view_status(self):
        resp = self.client.get(reverse("note_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "测试笔记")

    def test_list_view_requires_login(self):
        self.client.logout()
        resp = self.client.get(reverse("note_list"))
        self.assertRedirects(resp, reverse("login") + "?next=" + reverse("note_list"))

    def test_list_view_pagination(self):
        for i in range(25):
            Note.objects.create(title=f"笔记{i}", content=f"内容{i}", owner=self.user)
        resp = self.client.get(reverse("note_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["is_paginated"])
        self.assertEqual(len(resp.context["notes"]), 20)

    # ---- 用户隔离 ----

    def test_notes_isolated_by_user(self):
        Note.objects.create(title="他人的笔记", content="不应该看到", owner=self.other_user)
        resp = self.client.get(reverse("note_list"))
        self.assertContains(resp, "测试笔记")
        self.assertNotContains(resp, "他人的笔记")

    # ---- 详情视图 ----

    def test_detail_view(self):
        resp = self.client.get(reverse("note_detail", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "测试内容")

    def test_detail_view_other_user_forbidden(self):
        other_note = Note.objects.create(title="别人的", content="私密", owner=self.other_user)
        resp = self.client.get(reverse("note_detail", args=[other_note.pk]))
        self.assertEqual(resp.status_code, 404)

    # ---- 创建视图 ----

    def test_create_view_get(self):
        resp = self.client.get(reverse("note_create"))
        self.assertEqual(resp.status_code, 200)

    def test_create_view_post(self):
        resp = self.client.post(reverse("note_create"), {
            "title": "新笔记",
            "content": "新内容",
        })
        self.assertRedirects(resp, reverse("note_list"))
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(title="新笔记")
        self.assertEqual(new_note.content, "新内容")
        self.assertEqual(new_note.owner, self.user)

    # ---- 更新视图 ----

    def test_update_view_get(self):
        resp = self.client.get(reverse("note_update", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_update_view_post(self):
        resp = self.client.post(
            reverse("note_update", args=[self.note.pk]),
            {"title": "已更新", "content": "更新内容"},
        )
        self.assertRedirects(resp, reverse("note_list"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "已更新")
        self.assertEqual(self.note.content, "更新内容")

    def test_update_other_user_forbidden(self):
        other_note = Note.objects.create(title="别人的", content="私密", owner=self.other_user)
        resp = self.client.get(reverse("note_update", args=[other_note.pk]))
        self.assertEqual(resp.status_code, 404)

    # ---- 删除视图 ----

    def test_delete_view_get(self):
        resp = self.client.get(reverse("note_delete", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "确认删除")

    def test_delete_view_post(self):
        resp = self.client.post(reverse("note_delete", args=[self.note.pk]))
        self.assertRedirects(resp, reverse("note_list"))
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_other_user_forbidden(self):
        other_note = Note.objects.create(title="别人的", content="私密", owner=self.other_user)
        resp = self.client.post(reverse("note_delete", args=[other_note.pk]))
        self.assertEqual(resp.status_code, 404)

    # ---- 搜索功能 ----

    def test_search_icontains(self):
        Note.objects.create(title="Python学习笔记", content="Django框架实践", owner=self.user)
        resp = self.client.get(reverse("note_list") + "?q=Python")
        self.assertContains(resp, "Python学习笔记")
        self.assertNotContains(resp, "测试笔记")

    def test_search_regex(self):
        Note.objects.create(title="2024年度计划", content="", owner=self.user)
        resp = self.client.get(reverse("note_list") + r"?q=\d{4}年")
        self.assertContains(resp, "2024年度计划")

    def test_invalid_regex_fallback(self):
        resp = self.client.get(reverse("note_list") + "?q=[未闭合括号")
        self.assertEqual(resp.status_code, 200)

    # ---- 排序功能 ----

    def test_sort_by_created_at(self):
        n1 = Note.objects.create(title="B笔记", content="", owner=self.user)
        n2 = Note.objects.create(title="A笔记", content="", owner=self.user)
        resp = self.client.get(reverse("note_list") + "?sort=created_at")
        notes = list(resp.context["notes"])
        self.assertEqual(notes[0], self.note)

    def test_sort_by_title(self):
        Note.objects.create(title="Z笔记", content="", owner=self.user)
        Note.objects.create(title="A笔记", content="", owner=self.user)
        resp = self.client.get(reverse("note_list") + "?sort=title")
        notes = list(resp.context["notes"])
        self.assertEqual(notes[0].title, "A笔记")


class AuthViewTest(TestCase):
    def test_login_page(self):
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)

    def test_register_page(self):
        resp = self.client.get(reverse("register"))
        self.assertEqual(resp.status_code, 200)

    def test_register_creates_user(self):
        resp = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "Str0ngP@ssword!",
            "password2": "Str0ngP@ssword!",
        })
        self.assertRedirects(resp, reverse("note_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_redirects_authenticated(self):
        User.objects.create_user("existing", password="testpass")
        self.client.login(username="existing", password="testpass")
        resp = self.client.get(reverse("register"))
        self.assertRedirects(resp, reverse("note_list"))
