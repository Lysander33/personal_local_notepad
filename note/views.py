import re
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note
from .forms import NoteForm


class NoteListView(ListView):
    """笔记列表页，支持搜索与排序"""
    model = Note
    template_name = "note/note_list.html"
    context_object_name = "notes"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            # 优先正则匹配，失败则降级为模糊搜索
            try:
                re.compile(q)
                queryset = queryset.filter(
                    Q(title__regex=q) | Q(content__regex=q)
                )
            except re.error:
                queryset = super().get_queryset().filter(
                    Q(title__icontains=q) | Q(content__icontains=q)
                )
        # 排序：白名单校验
        sort = self.request.GET.get("sort", "-updated_at")
        allowed_sorts = {
            "-updated_at", "updated_at",
            "-created_at", "created_at",
            "title", "-title",
        }
        if sort in allowed_sorts:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_q"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "-updated_at")
        return context


class NoteDetailView(DetailView):
    """笔记详情页"""
    model = Note
    template_name = "note/note_detail.html"
    context_object_name = "note"


class NoteCreateView(CreateView):
    """新建笔记"""
    model = Note
    form_class = NoteForm
    template_name = "note/note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"笔记「{self.object.title}」创建成功")
        return response


class NoteUpdateView(UpdateView):
    """编辑笔记"""
    model = Note
    form_class = NoteForm
    template_name = "note/note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"笔记「{self.object.title}」更新成功")
        return response


class NoteDeleteView(DeleteView):
    """删除笔记"""
    model = Note
    template_name = "note/note_confirm_delete.html"
    success_url = reverse_lazy("note_list")
    context_object_name = "note"

    def form_valid(self, form):
        messages.success(self.request, f"笔记「{self.object.title}」已删除")
        return super().form_valid(form)
