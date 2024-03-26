from django.http import HttpResponse
from django.shortcuts import render, redirect
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with '/receiver'
        if request.path.startswith('/receiver'):
            # Perform authentication checks here
            if not request.session.get('user_id') or not request.session.get('role') == 'receiver':
                return redirect('/login')
        
        # Allow the request to proceed to other middleware or view functions if it dont start with '/receiver' or the user is authenticated
  
        response = self.get_response(request)
        return response
