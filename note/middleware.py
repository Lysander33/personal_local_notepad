from django.conf import settings
from django.http import HttpResponseForbidden


class LocalOnlyMiddleware:
    """本地模式中间件：当 LOCAL_MODE=True 时，仅允许本机访问。

    检查 REMOTE_ADDR，非本机 IP 直接返回 403。
    LOCAL_MODE=False 时不做限制。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "LOCAL_MODE", True):
            remote_addr = request.META.get("REMOTE_ADDR", "")
            if remote_addr not in ("127.0.0.1", "::1"):
                return HttpResponseForbidden("仅限本机访问")
        return self.get_response(request)
