from django.http import HttpRequest, HttpResponse
from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from .models import Book


def set_useragent_on_request_middleware(get_response):
    print('initial cell')

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests_count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses_count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print('got', self.exception_count, 'exceptions so far')


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.responses_dict = {}
        self.time_delta = timedelta(seconds=0.01)

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        date_now = datetime.now()

        if request.META.get('REMOTE_ADDR') not in self.responses_dict:
            self.responses_dict[request.META.get('REMOTE_ADDR')] = date_now
            return response

        delta = date_now - self.responses_dict[request.META.get('REMOTE_ADDR')]

        self.responses_dict[request.META.get('REMOTE_ADDR')] = date_now

        if delta < self.time_delta:
            # return HttpResponse('Throttling alert!')
            context = {
                'items': Book.objects.all(),
            }
            return render(request, 'requestdataapp/throttling.html', context=context)

        return response
