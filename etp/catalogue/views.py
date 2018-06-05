from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from .models import Book
from .forms import BookForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from registration.models import Profile

# Decorador propio para las vistas 

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


# Create your views here.


class CatalogueListView(ListView):
    model = Book
    paginate_by = 4
    

@method_decorator(login_required, name='dispatch')
class BookDetailView(DetailView):
    model = Book

@method_decorator(group_required('Proveedor'),name='dispatch')
class BookCreate(CreateView):
    model = Book
    form_class = BookForm
    
    def get_success_url(self):
        return reverse_lazy('catalogue:books')+'?okcreate'

    def get_form_kwargs(self):
        kwargs = super(BookCreate, self).get_form_kwargs()
        kwargs.update({'place_user': self.request.user})
        return kwargs
    

@method_decorator(group_required('Proveedor'),name='dispatch')
class BookUpdate(UpdateView):
    model = Book
    form_class = BookForm
       
    template_name_suffix = '_update_form'

    def get_success_url(self):
        x = self.kwargs
        return reverse_lazy('catalogue:update',kwargs={'pk': x['pk']})+'?ok'


@method_decorator(group_required('Proveedor'),name='dispatch')
class BookDelete(DeleteView):
    model = Book
    def get_success_url(self):
        return reverse_lazy('catalogue:books')+'?okdelete'


def BookOrder(request,id):
    book = Book.objects.get(id=id)
    x = request.user
    cliente = Profile.objects.get(user=request.user)
    cliente2 = book.client.all()

    if cliente in cliente2:
        return HttpResponseRedirect(reverse('catalogue:books')+'?notorder')
    else:
        book.client.add(cliente)
        book.quantity = book.quantity + 1
        book.save()
        return HttpResponseRedirect(reverse('catalogue:books')+'?okorder')
