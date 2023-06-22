from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from django.core.paginator import Paginator
from django.db.models import Q
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context



def product_view(request):
    products = Product.objects.all()
    variants = ProductVariant.objects.all()
    product_info = ProductVariantPrice.objects.all()

    total_product = len(products)

    paginator = Paginator(product_info, 2)  # Show 2 product details per page.
    page_number = request.GET.get('page')
    product_info_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'variants': variants,
        'product_info': product_info,
        'total_product': total_product,
        'product_info_obj': product_info_obj
    }

    return render(request, "products/list.html", context)


def search_view(request):
    product_info = None

    if request.method == "POST":
        title_search = request.POST["product_title"]
        variant_search = request.POST["variant_search"]
        price_from = request.POST["price_from"]
        price_to = request.POST["price_to"]

        variants = ProductVariant.objects.all()
        
     
        try:
            price_from = float(price_from)
        except ValueError:
            price_from = None

        try:
            price_to = float(price_to)
        except ValueError:
            price_to = None

       
        query = Q(product__title__contains=title_search) | Q(product_variant_one__variant_title__contains=variant_search)
        if price_from is not None:
            query &= Q(price__gte=price_from)
        if price_to is not None:
            query &= Q(price__lte=price_to)

        product_info = ProductVariantPrice.objects.filter(query)

    context = {
        'product_info': product_info,
        'variants': variants
    }

    return render(request, "products/product_search.html", context)
