import re

from django.contrib.sessions.models import Session
from wagtail.models import PageViewRestriction

from blog.models import BlogDetailPage


class PagePasswordUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if ma := re.match(r"^/admin/pages/(\d+)/privacy/$", request.path):
            id_ = ma.group(1)
            if request.POST.get("restriction_type") == PageViewRestriction.PASSWORD:
                page = BlogDetailPage.objects.get(id=id_)
                restriction = page.get_password_restriction()
                k = restriction.passed_view_restrictions_session_key

                sessions = Session.objects.all()

                for session in sessions:
                    session_data = session.get_decoded()
                    if k in session_data:
                        passed_restrictions = session_data[k]
                        if restriction.id not in passed_restrictions:
                            continue
                        passed_restrictions.remove(restriction.id)
                        session_data[k] = passed_restrictions
                        session.session_data = Session.objects.encode(session_data)
                        session.save()

        return response
