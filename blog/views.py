import json

from django.http import JsonResponse
from .models import BlogDetailPage


def get_links_options(request):
    if request.method == 'GET':
        pages = BlogDetailPage.objects.all()
        result = []
        for page in pages:
            obj = json.loads(page.to_json())
            page_title = obj.get('title', '')
            if not page_title:
                continue
            result.append(page_title)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
