import json

from django.http import JsonResponse
from .models import BlogDetailPage


def get_links_options(request):
    if request.method == 'GET':
        pages = BlogDetailPage.objects.all()
        all_links = []
        for page in pages:
            obj = json.loads(page.to_json())
            link_array = obj.get('links', [])
            link_array = json.loads(link_array) if link_array else []
            for link_block in link_array:
                value = link_block.get('value', {})
                if not value:
                    continue
                all_links.append(
                    {
                        'title': value.get('title', ''),
                        'url': value.get('url', ''),
                    }
                )
        return JsonResponse(all_links, safe=False)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
