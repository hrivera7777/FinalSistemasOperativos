from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "core/base.html"

    
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{'title': "Ch Máquina"} )
# Create your views here.
