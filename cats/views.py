from django.shortcuts import render
from cats.models import Breed, Cat

def index(request):
    context = {
        'objects_list': Breed.objects.all()[:3],
        'title': 'Питомник кошек - Главная',
    }
    return render(request, 'cats/index.html', context)

def breeds_list(request):
    context = {
        'objects_list': Breed.objects.all(),
        'title': 'Все породы кошек',
    }
    return render(request, 'cats/breeds.html', context)

def breeds_cats_list(request, pk: int):
    breed_item = Breed.objects.get(pk=pk)
    context = {
        'objects_list': Cat.objects.filter(breed_id=pk),
        'title': f'Кошки породы {breed_item}',
        'breed_pk': breed_item.pk,
    }
    return render(request, 'cats/cats.html', context)

def cats_list_view(request):
    context = {
        'objects_list': Cat.objects.all(),
        'title': 'Все наши кошки',
    }
    return render(request, 'cats/cats.html', context)