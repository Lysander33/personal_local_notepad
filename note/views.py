import re
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .forms import NoteForm, RegisterForm
from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "note/note_list.html"
    context_object_name = "notes"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        q = self.request.GET.get("q", "").strip()
        if q:
            try:
                re.compile(q)
                queryset = queryset.filter(
                    Q(title__regex=q) | Q(content__regex=q)
                )
            except re.error:
                queryset = queryset.filter(
                    Q(title__icontains=q) | Q(content__icontains=q)
                )
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


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "note/note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note/note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"笔记「{self.object.title}」创建成功")
        return response


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note/note_form.html"
    success_url = reverse_lazy("note_list")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"笔记「{self.object.title}」更新成功")
        return response


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "note/note_confirm_delete.html"
    success_url = reverse_lazy("note_list")
    context_object_name = "note"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"笔记「{self.object.title}」已删除")
        return super().form_valid(form)


class NoteLoginView(LoginView):
    template_name = "note/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "登录成功")
        return super().form_valid(form)


class NoteRegisterView(FormView):
    template_name = "note/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("note_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("note_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        messages.success(self.request, f"欢迎 {user.username}，注册成功")
        return super().form_valid(form)
