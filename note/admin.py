from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """笔记管理后台配置"""
    list_display = ["title", "content_preview", "created_at", "updated_at"]
    search_fields = ["title", "content"]
    list_filter = ["created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]

    @admin.display(description="内容预览")
    def content_preview(self, obj):
        """返回内容的前100字预览"""
        if len(obj.content) > 100:
            return obj.content[:100] + "..."
        return obj.content
