# 个人本地记事本

基于 Django 的轻量级笔记应用。

## 快速开始

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

访问 <http://127.0.0.1:8000/>。

## 功能

- 笔记 CRUD（新建、查看、编辑、删除）
- 搜索（支持正则表达式）
- 排序（更新时间 / 创建时间 / 标题）
- 分页
- 响应式布局（桌面侧边栏 + 移动端适配）

## 项目结构

```
DjangoProject/          # 项目配置：settings、URL 根路由
note/                   # 笔记应用
  models.py             # Note 模型（标题、内容、时间戳）
  views.py              # 基于类的通用视图
  forms.py              # NoteForm
  urls.py               # 应用路由
  tests.py              # 14 个测试用例
  templates/note/       # 页面模板
  static/note/css/      # 自定义样式
```

## 技术栈

- Python 3 + Django 6.0
- SQLite
- Bootstrap 5 (CDN)
- 自定义 CSS（CSS Variables + 响应式断点）

## 测试

```bash
python manage.py test note
```
