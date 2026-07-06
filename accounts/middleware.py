from django.utils import timezone
from .models import UserProfile


class UpdateLastSeenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if hasattr(request, "user") and request.user.is_authenticated:

            profile, created = UserProfile.objects.get_or_create(
                user=request.user
            )

            profile.last_seen = timezone.now()
            profile.save(update_fields=["last_seen"])

        response = self.get_response(request)

        return response
