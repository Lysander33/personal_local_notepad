from django.db import models


class Note(models.Model):
    """笔记模型"""
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "笔记"
        verbose_name_plural = "笔记"

    def __str__(self):
        return self.title
