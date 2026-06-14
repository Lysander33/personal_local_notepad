#!/usr/bin/env bash
set -e
echo "========================"
echo "  个人记事本 — 一键启动"
echo "========================"
echo

cd "$(dirname "$0")"

if [ ! -f ".env" ]; then
    echo "[提示] 未检测到 .env 文件，从 .env.example 复制..."
    cp .env.example .env
fi

echo "[1/2] 初始化数据库..."
python manage.py migrate --noinput

echo "[2/2] 启动服务器 http://127.0.0.1:8000/"
echo
python manage.py runserver
