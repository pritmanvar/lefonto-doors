from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from catalog.models import Image

@login_required
def file_handler(request):
    try:
        if request.method == 'POST':
            file = request.FILES['file']
            if not file:
                return HttpResponseBadRequest("No file provided.")

            obj = Image(image=file)
            obj.save()

            return JsonResponse({'value': obj.image.url})

        elif request.method == 'GET':
            page = int(request.GET.get('page', 1))

            files_per_page = 10

            start = (page - 1) * files_per_page
            end = start + files_per_page

            results = []

            for obj in Image.objects.all()[start:end]:
                results.append({
                    'value': obj.image.name,
                    'thumbnail': obj.image.url,
                    'metadata': {
                        'name': obj.image.name.split('/')[-1],
                    }
                })

            return JsonResponse({'results': results})
        # Catch-all fallback
        return HttpResponseBadRequest("Only GET and POST methods are allowed.")

    except Exception as e:
        return HttpResponseBadRequest(f"Internal Error: {str(e)}")
