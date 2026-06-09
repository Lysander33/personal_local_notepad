# 个人本地记事本

基于 Django 的轻量级笔记应用。

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python manage.py migrate

# 3. 配置环境（可选）
cp .env.example .env

# 4. 启动服务器
python manage.py runserver
```

访问 <http://127.0.0.1:8000/>。

## 配置说明

### 环境变量（.env）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | Django 密钥 | `django-insecure-dev-fallback` |
| `DEBUG` | 调试模式 | `True` |
| `LOCAL_MODE` | 本地模式（仅本机访问） | `True` |

### 模式切换

- **本地模式**（默认）：`python manage.py runserver`，仅本机可访问
- **分享模式**：先改 `.env` 中 `LOCAL_MODE=False`，再 `python manage.py runserver 0.0.0.0:8000`

## 在手机或他人电脑上使用

1. 编辑 `.env`，将 `LOCAL_MODE` 改为 `False`：
   ```
   LOCAL_MODE=False
   ```

2. 启动服务器：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   确保电脑和手机在同一 WiFi 下。

3. 控制台会显示局域网 IP 地址，在手机浏览器访问即可。

> 用完记得改回 `LOCAL_MODE=True`，重新以 `python manage.py runserver` 启动。

## 功能

- 笔记 CRUD（新建、查看、编辑、删除）
- 搜索（支持正则表达式，自动降级为模糊搜索）
- 排序（更新时间 / 创建时间 / 标题）
- 分页
- 响应式布局（桌面侧边栏 + 移动端适配）
- 操作反馈提示

## 项目结构

```
DjangoProject/          # 项目配置：settings、URL 根路由
note/                   # 笔记应用
  models.py             # Note 模型（标题、内容、时间戳）
  views.py              # 基于类的通用视图
  forms.py              # NoteForm
  urls.py               # 应用路由
  admin.py              # Admin 后台配置
  middleware.py          # 本地访问限制中间件
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
