from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from resgain.models import Surnames, Names


def index(request):
    if request.method == 'GET':
        xs = Surnames.objects.all()
        xs_list = []
        list1 = []
        for item in range(len(xs)):
            list1.append(xs[item])
            if len(list1) == 7:
                xs_list.append(list1)
                list1 = []
        # print(xs_list)
        return render(request, 'index.html', {'xs_list': xs_list})


def names(request, i):
    if request.method == 'GET':
        # return render(request, 'names.html')
        names = Names.objects.filter(surname=i)
        name_list = []
        list1 = []
        for item in range(len(names)):
            list1.append(names[item])
            if len(list1) == 15:
                name_list.append(list1)
                list1 = []

        try:
            page_number = int(request.GET.get('page', 1))
        except:
            page_number = 1

        paginator = Paginator(name_list, 20)
        pages = paginator.page(page_number)

        return render(request, 'names.html', {'pages': pages, 'i': i})


def info(request, i):
    if request.method == 'GET':
        name = Names.objects.filter(name=i)
        return render(request, 'info.html', {'name': name, 'i': i})