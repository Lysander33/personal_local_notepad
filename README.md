# 个人记事本

基于 Django 的轻量级多用户笔记应用，支持 Markdown，开箱即用。

## 快速开始

```bash
# 1. 克隆项目后安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python manage.py migrate

# 3. （可选）创建管理员账号
python manage.py createsuperuser

# 4. 启动
python manage.py runserver
```

访问 <http://127.0.0.1:8000/>，注册账号即可使用。

## 一键启动

```bash
# Windows
start.bat

# macOS / Linux
bash start.sh
```

## 配置说明

通过 `.env` 文件配置（复制 `.env.example` 为 `.env`）：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Django 密钥 | `django-insecure-dev-fallback` |
| `DEBUG` | 调试模式 | `True` |
| `LOCAL_MODE` | 本地模式（仅本机访问） | `True` |
| `CSRF_TRUSTED_ORIGINS` | CSRF 可信来源（部署时配置） | 空 |

### 模式切换

- **本地模式**（默认）：`python manage.py runserver`，仅本机可访问
- **分享模式**：改 `.env` 中 `LOCAL_MODE=False`，再 `python manage.py runserver 0.0.0.0:8000`

## 功能

- 多用户注册/登录，笔记按用户隔离
- 笔记 CRUD（新建、查看、编辑、删除）
- Markdown 内容渲染（支持代码块、表格、自动换行）
- 搜索（支持正则表达式，自动降级为模糊搜索）
- 排序（更新时间 / 创建时间 / 标题）
- 分页
- 响应式布局（桌面侧边栏 + 移动端适配）
- Django Admin 后台管理

## 项目结构

```
DjangoProject/          # 项目配置：settings、URL 根路由
note/                   # 笔记应用
  models.py             # Note 模型（标题、内容、所有者、时间戳）
  views.py              # 基于类的通用视图（含认证保护）
  forms.py              # NoteForm + RegisterForm
  urls.py               # 应用路由 + 认证路由
  admin.py              # Admin 后台配置
  middleware.py          # 本地访问限制中间件
  tests.py              # 18 个测试用例
  templates/note/       # 页面模板
  static/note/css/      # 自定义样式
```

## 技术栈

- Python 3 + Django 6.0
- SQLite
- Markdown (python-markdown)
- Bootstrap 5 (CDN)
- 自定义 CSS（CSS Variables + 响应式断点）

## 测试

```bash
python manage.py test note
```

## 生产部署

1. 设置 `.env`：`DEBUG=False`，生成随机 `SECRET_KEY`，配置 `CSRF_TRUSTED_ORIGINS`
2. 收集静态文件：`python manage.py collectstatic`
3. 使用 Gunicorn/uWSGI + Nginx 部署
4. 建议切换数据库为 PostgreSQL
