from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt


class HomeView(TemplateView):

    template_name = '/BS/index.html'



# def menu1(request):
#     template = './busan_6.html'
#     context = {'template':template}
#     return render(request, 'menu1.html', context=context)

# def menu2(request):
#     template = './busan_Total.html'
#     context = {'template':template}
#     return render(request, 'menu2.html', context=context)