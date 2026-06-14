# 个人记事本

轻量级多用户笔记应用，Markdown 渲染，开箱即用。每人独立账号，笔记互不可见。

## 快速开始

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

打开 http://127.0.0.1:8000 注册即用。

> 也可直接运行 `start.bat`（Windows）或 `bash start.sh`（macOS/Linux）一键启动。

## 配置

复制 `.env.example` 为 `.env`：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Django 密钥，部署前**必须**更换 | `django-insecure-dev-fallback` |
| `DEBUG` | 调试模式 | `True` |
| `LOCAL_MODE` | `True`=仅本机 / `False`=对外开放 | `True` |
| `CSRF_TRUSTED_ORIGINS` | 部署域名，逗号分隔 | 空 |

## 功能

多用户注册/登录 · 笔记 CRUD · Markdown 渲染（代码高亮、表格、换行） · 搜索（正则 + 模糊降级） · 排序（时间/标题） · 分页 · 响应式布局 · Admin 后台 · 本地/分享模式切换

## 安全

用户隔离（owner 过滤） · PBKDF2 密码哈希 · CSRF 防护 · XSS 防护（Markdown 转义 + X-Frame-Options） · ORM 参数化查询

部署前务必更换 `SECRET_KEY`、关 `DEBUG`、启 HTTPS。

## 技术栈

Python 3 · Django 6.0 · SQLite（可换 PostgreSQL/MySQL） · Bootstrap 5 CDN · python-markdown

## 测试

```bash
python manage.py test note
```

26 个用例，覆盖模型、CRUD、认证、隔离、搜索、排序、分页。

## 生产部署

```bash
# 1. 环境配置
cp .env.example .env
# 编辑：SECRET_KEY=<随机生成> DEBUG=False LOCAL_MODE=False CSRF_TRUSTED_ORIGINS=https://你的域名

# 2. 初始化
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# 3. 启动（Gunicorn）
gunicorn DjangoProject.wsgi -b 0.0.0.0:8000 -w 4
```

Nginx 反代 + HTTPS（Let's Encrypt）：

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    location /static/ { alias /path/to/staticfiles/; }
    location / { proxy_pass http://127.0.0.1:8000; proxy_set_header Host $host; }
}
```

## 项目结构

```
DjangoProject/          # 项目配置
note/                   # 笔记应用
  models.py             # Note 模型 + Markdown 渲染
  views.py              # CBV + 登录注册 + owner 过滤
  forms.py              # NoteForm + RegisterForm
  urls.py               # 路由（笔记 + 认证）
  admin.py              # Admin 配置
  middleware.py          # LOCAL_MODE 访问控制
  tests.py              # 26 个测试用例
  templates/note/       # 6 个页面模板
  static/note/css/      # 自定义样式
```