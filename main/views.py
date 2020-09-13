from django.shortcuts import redirect
from django.views import View


class MainIndex(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news')
