from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cats.models import Breed, Cat
from cats.forms import CatForm
from users.services import send_cat_creation


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

# --- НОВЫЕ ФУНКЦИИ CRUD ---
def cat_detail_view(request, pk):
    """Просмотр одной кошки"""
    cat = get_object_or_404(Cat, pk=pk)
    context = {
        'object': cat,
        'title': f'Кошка {cat.name}'
    }
    return render(request, 'cats/cat_detail.html', context)


@login_required()
def cat_create_view(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)

        if form.is_valid():
            cat_object = form.save(commit=False)  # Не сохраняем сразу!
            cat_object.owner = request.user  # Назначаем хозяина
            cat_object.save()  # Теперь сохраняем

            # ОТПРАВКА ПИСЬМА
            send_cat_creation(cat_object.owner.email, cat_object)

            return redirect('cats:cats_list')  # адрес списка кошек

    context = {'form': CatForm(), 'title': 'Добавить кошку'}
    return render(request, 'cats/create_update.html', context)


def cat_update_view(request, pk):
    """Редактирование кошки"""
    cat = get_object_or_404(Cat, pk=pk)

    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('cats:cat_detail', pk=pk)

    context = {
        'form': CatForm(instance=cat),
        'object': cat,
        'title': f'Изменить кошку {cat.name}'
    }
    return render(request, 'cats/create_update.html', context)


def cat_delete_view(request, pk):
    """Удаление кошки"""
    cat = get_object_or_404(Cat, pk=pk)
    if request.method == 'POST':
        cat.delete()
        return redirect('cats:cats_list')

    context = {'object': cat, 'title': f'Удалить кошку {cat.name}'}
    return render(request, 'cats/delete.html', context)
