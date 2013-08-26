from django.http import HttpResponse

def update_location(request):
    if request.method == 'POST':
            print 'Raw Data: "%s"' % request.raw_post_data
            return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)