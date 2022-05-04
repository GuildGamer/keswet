from django.http import JsonResponse
from django.utils import timezone


def home(request) -> JsonResponse:
    now = timezone.now()
    return JsonResponse(
        {"alive": True, "timestamp": now, "api_version": "1.0.0", "srv": "keswet"}
    )
