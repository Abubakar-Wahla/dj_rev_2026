from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": "ok", "service": "dj_rev_2026 api"})
