from django.shortcuts import render


def dummy(request):
    return render(request, 'dummy/dummy.html')
