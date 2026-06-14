@echo off
chcp 65001 >nul
echo ========================
echo   个人记事本 — 一键启动
echo ========================
echo.
cd /d "%~dp0"

if not exist ".env" (
    echo [提示] 未检测到 .env 文件，从 .env.example 复制...
    copy .env.example .env >nul
)

echo [1/2] 初始化数据库...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo 数据库迁移失败，请检查错误信息。
    pause
    exit /b %errorlevel%
)

echo [2/2] 启动服务器 http://127.0.0.1:8000/
echo.
python manage.py runserver
pause
