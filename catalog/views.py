from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from catalog.models import Image

@login_required
def file_handler(request):
    if request.method == 'POST':
        file = request.FILES['file']
        obj = Image(image=file)
        obj.save()

        return JsonResponse({'value': obj.image.url})
