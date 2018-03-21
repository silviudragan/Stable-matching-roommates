from django.shortcuts import render
from django.views import View


class Administrator(View):
    template_name = 'stable/admin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self):
        pass
