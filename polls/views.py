# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters
# from dotenv import load_dotenv
import os
from django.views.decorators.csrf import csrf_exempt

# load_dotenv()
def implements_str(cls):
    cls.__unicode__ = cls.__str__
    cls.__str__ = lambda x: unicode(x).encode("utf-8")  # noqa
    return cls

def index(request):
    return HttpResponse("Hello, world. You're at the polls index. This is now an updated version.")

def index2(request):
    return HttpResponse("This is new hello world.")

def simple_decorator(func):
    def wrapper(*args, **kwargs):
        # Call the decorated function
        simple_decorator_variable = 'No way'
        user = 'wrapper user'
        after_after_req = 'wrapper var'
        result = func(*args, **kwargs)
        return result
    return wrapper


@sensitive_variables('user')
def trigger_error(request):
    user = "user"
    pwd = "other_id"
    a = 1
    b= 0
    raise IndentationError
    return 0

@simple_decorator
@sensitive_variables()
def trigger_error1(request):
    user = os.getenv("user")
    pwd = os.getenv("other_id")
    a = 1
    b= 0
    raise ImportError
    return 0

@sensitive_variables()
@simple_decorator
def trigger_error2(request):
    user = os.getenv("user")
    pwd = os.getenv("other_id")
    a = 1
    b= 0
    raise MemoryError
    return 0

@sensitive_variables('after_after_req')
def after_after_req(user):
    after_after_req = 'var'
    raise ImportError

def after_req(user):
    after_req = 'var'
    return after_after_req(user)

@sensitive_variables("user", "pwd")
@simple_decorator
def trigger_error3(request):
    user = os.getenv("user")
    pwd = os.getenv("other_id")
    after_after_req  = 'dummy after_after_req'
    a = 1
    b= 0
    return after_req(user)


@sensitive_post_parameters("pass_word", "credit_card_number")
@sensitive_variables("password","credit_card")
@csrf_exempt
def record_user_profile(request):
    password=request.POST["pass_word"]
    credit_card=request.POST["credit_card_number"]
    name=request.POST["name"]
    raise LookupError
    return JsonResponse({'msg': 'valid data'}, status=200)

def decorator_with_sensitive_data(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        to_be_hidden = request.POST["to_be_hidden"]
        print("{}".format(to_be_hidden))
        return func(*args, **kwargs)

    return wrapper


@sensitive_variables("to_be_hidden")
@decorator_with_sensitive_data
def hide_nested_sensitive_data(request):
    @sensitive_variables("after_after_req_var")
    def after_after_req(to_be_hidden):
        after_after_req_var = "foo"
        print("{}".format(after_after_req_var))
        1 / 0

    def after_req(to_be_hidden):
        return after_after_req(to_be_hidden)

    to_be_hidden = "to_be_hidden"
    to_not_be_hidden = "to_not_be_hidden"
    print("{}".format(to_not_be_hidden))
    return after_req(to_be_hidden)