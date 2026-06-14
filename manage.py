#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoProject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from django.conf import settings
    if settings.SECRET_KEY == "django-insecure-dev-fallback" and "runserver" in sys.argv:
        import sys as _sys
        _sys.stderr.write(
            "\n[WARNING] 正在使用默认 SECRET_KEY，生产环境请通过 .env 文件设置随机密钥\n\n"
        )

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
