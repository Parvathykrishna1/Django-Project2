from django.utils.functional import wraps
from django.shortcuts import render, redirect
from accounts.views import userLogin
from django.contrib.auth import authenticate


from django.shortcuts import redirect


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated and request.path != "/login/":
            return render(request, "accounts/login.html")

        response = self.get_response(request)
        return response
