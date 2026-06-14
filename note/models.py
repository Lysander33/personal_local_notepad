from django.contrib.auth.models import User
from django.db import models
from markdown import markdown


class Note(models.Model):
    """笔记模型"""
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所有者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "笔记"
        verbose_name_plural = "笔记"

    @property
    def content_html(self):
        return markdown(self.content, extensions=["fenced_code", "tables", "nl2br"])

    def __str__(self):
        return self.title
