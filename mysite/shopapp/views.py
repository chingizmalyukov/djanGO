from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Product, Order
from .forms import ProductForm, OrderForm, GroupForms
from django.views import View


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [('desktop', 2999),
                    ('laptop', 1999),
                    ('smartphone', 999)
                    ]
        context = {
            'products': products
        }

        return render(request, 'shopapp/index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForms(),
            'groups': Group.objects.prefetch_related('permissions').all(),
            # prefetch_related - загружает сразу все сущности, если будет 10 групп, то будет сделан 1 запрос, а не 10
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForms(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = 'product'


class ProductsView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class OrderCreateView(CreateView):
    model = Order
    fields = 'user', 'products', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects
                .select_related('user')
                .prefetch_related('products')
                )


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = ['shopapp.view_order', ]
    queryset = (Order.objects
                .select_related('user')
                .prefetch_related('products')
                )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'products', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk}
        )


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'shopapp.add_product'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:

            perms = self.get_permission_required()
            # created_by = (Product.objects
            #     .select_related('created_by')
            #     .prefetch_related('pk')
            #     )
            # # created_by = Product.objects.get('created_by_id').all
            # print(f'CREATED BY {created_by}')
            if self.request.user.has_perms(perms):
                return True

    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )
