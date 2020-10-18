from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render


def visitor_signup_view(request):
    form = UserCreationForm()
    # form_class = UserCreationForm()
    # success_url = reverse_lazy('login')
    # template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'registration/signup.html', context)

# class visitor_login_view(generic.CreateView):
#     form_class = UserCreationForm