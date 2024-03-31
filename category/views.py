from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Category, FavoriteCategory
from django.core.paginator import Paginator

@login_required
def home(request):
    categories = Category.objects.all()
    favorites = FavoriteCategory.objects.filter().values_list('id', flat=True)

    # Paginate 
    page_number = request.GET.get('page')
    limit = request.GET.get('limit',6)

    paginator = Paginator(categories, limit)  
    page_obj = paginator.get_page(page_number)

    data = []
    for instance in page_obj:
        coin_data = {
            'name': instance.name,
            'is_favorite': instance.id in favorites
        }
        data.append(coin_data)

    return JsonResponse({
        'results': data,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'current_page': page_obj.number
    })

@login_required
def add_favorite(request, id):
    category = get_object_or_404(Category, pk=id)
    favorite, created = FavoriteCategory.objects.get_or_create(user=request.user, category=category)
    return redirect('home')