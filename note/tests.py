from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    """Note 模型测试"""

    def test_create_note(self):
        """测试创建笔记"""
        note = Note.objects.create(title="测试笔记", content="这是测试内容")
        self.assertEqual(str(note), "测试笔记")
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)

    def test_default_ordering(self):
        """测试默认按更新时间倒序排列"""
        n1 = Note.objects.create(title="旧笔记", content="先创建的")
        n2 = Note.objects.create(title="新笔记", content="后创建的")
        notes = list(Note.objects.all())
        self.assertEqual(notes[0], n2)  # 最新排第一


class NoteViewTest(TestCase):
    """Note 视图测试"""

    def setUp(self):
        self.note = Note.objects.create(title="测试笔记", content="测试内容")

    # ---- 列表视图 ----

    def test_list_view_status(self):
        """测试列表页正常访问"""
        resp = self.client.get(reverse("note_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "测试笔记")

    def test_list_view_pagination(self):
        """测试分页功能"""
        for i in range(25):
            Note.objects.create(title=f"笔记{i}", content=f"内容{i}")
        resp = self.client.get(reverse("note_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["is_paginated"])
        self.assertEqual(len(resp.context["notes"]), 20)

    # ---- 详情视图 ----

    def test_detail_view(self):
        """测试详情页正常访问"""
        resp = self.client.get(reverse("note_detail", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "测试内容")

    # ---- 创建视图 ----

    def test_create_view_get(self):
        """测试新建笔记页面"""
        resp = self.client.get(reverse("note_create"))
        self.assertEqual(resp.status_code, 200)

    def test_create_view_post(self):
        """测试新建笔记提交"""
        resp = self.client.post(reverse("note_create"), {
            "title": "新笔记",
            "content": "新内容",
        })
        self.assertRedirects(resp, reverse("note_list"))
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(title="新笔记")
        self.assertEqual(new_note.content, "新内容")

    # ---- 更新视图 ----

    def test_update_view_get(self):
        """测试编辑笔记页面"""
        resp = self.client.get(reverse("note_update", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_update_view_post(self):
        """测试编辑笔记提交"""
        resp = self.client.post(
            reverse("note_update", args=[self.note.pk]),
            {"title": "已更新", "content": "更新内容"},
        )
        self.assertRedirects(resp, reverse("note_list"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "已更新")
        self.assertEqual(self.note.content, "更新内容")

    # ---- 删除视图 ----

    def test_delete_view_get(self):
        """测试删除确认页面"""
        resp = self.client.get(reverse("note_delete", args=[self.note.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "确认删除")

    def test_delete_view_post(self):
        """测试删除笔记提交"""
        resp = self.client.post(reverse("note_delete", args=[self.note.pk]))
        self.assertRedirects(resp, reverse("note_list"))
        self.assertEqual(Note.objects.count(), 0)

    # ---- 搜索功能 ----

    def test_search_icontains(self):
        """测试关键词模糊搜索"""
        Note.objects.create(title="Python学习笔记", content="Django框架实践")
        resp = self.client.get(reverse("note_list") + "?q=Python")
        self.assertContains(resp, "Python学习笔记")
        self.assertNotContains(resp, "测试笔记")

    def test_search_regex(self):
        """测试正则表达式搜索"""
        Note.objects.create(title="2024年度计划", content="")
        resp = self.client.get(reverse("note_list") + r"?q=\d{4}年")
        self.assertContains(resp, "2024年度计划")

    def test_invalid_regex_fallback(self):
        """测试非法正则表达式自动降级为模糊搜索（不报500错误）"""
        resp = self.client.get(reverse("note_list") + "?q=[未闭合括号")
        self.assertEqual(resp.status_code, 200)

    # ---- 排序功能 ----

    def test_sort_by_created_at(self):
        """测试按创建时间排序"""
        n1 = Note.objects.create(title="B笔记", content="")
        n2 = Note.objects.create(title="A笔记", content="")
        resp = self.client.get(reverse("note_list") + "?sort=created_at")
        notes = list(resp.context["notes"])
        self.assertEqual(notes[0], self.note)  # 最早的排第一

    def test_sort_by_title(self):
        """测试按标题字母排序"""
        Note.objects.create(title="Z笔记", content="")
        Note.objects.create(title="A笔记", content="")
        resp = self.client.get(reverse("note_list") + "?sort=title")
        notes = list(resp.context["notes"])
        self.assertEqual(notes[0].title, "A笔记")
