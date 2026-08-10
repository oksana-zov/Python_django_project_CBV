from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.forms import inlineformset_factory

from cats.models import Breed, Cat, Pedigree
from cats.forms import CatForm, CatCreateForm, PedigreeForm
from users.services import send_cat_creation


# 1. ГЛАВНАЯ СТРАНИЦА (Список пород)
class IndexView(ListView):
    model = Breed
    template_name = 'cats/index.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # Показываем только первые 3 породы
        return super().get_queryset()[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник кошек - Главная'
        return context


# 2. СПИСОК ВСЕХ ПОРОД
class BreedsListView(ListView):
    model = Breed
    template_name = 'cats/breeds.html'
    context_object_name = 'objects_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все породы кошек'
        return context


# 3. КОШКИ КОНКРЕТНОЙ ПОРОДЫ (с фильтрацией активности)
class BreedCatsListView(ListView):
    model = Cat
    template_name = 'cats/cats.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # Фильтруем по породе из URL И только активных кошек
        return super().get_queryset().filter(
            breed_id=self.kwargs.get('pk'),
            is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем объект породы для заголовка
        from cats.models import Breed
        breed = Breed.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = f'Кошки породы {breed.name}'
        context['breed_pk'] = breed.pk
        return context


# 4. ОБЩИЙ СПИСОК КОШЕК (только активные)
class CatsListView(ListView):
    model = Cat
    template_name = 'cats/cats.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # Скрываем неактивных кошек из публичного списка
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все наши кошки'
        return context


# 5. ДЕТАЛЬНАЯ СТРАНИЦА КОШКИ
class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/cat_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Кошка {self.object.name}'

        # Проверяем права для отображения кнопок редактирования/удаления
        user = self.request.user
        if user.is_authenticated:
            is_owner = self.object.owner == user
            is_staff = user.role in ['admin', 'moderator']
            context['can_edit'] = is_owner or is_staff
        else:
            context['can_edit'] = False

        return context


# 6. СОЗДАНИЕ КОШКИ
class CatCreateView(LoginRequiredMixin, CreateView):
    model = Cat
    form_class = CatCreateForm
    template_name = 'cats/create_update.html'
    success_url = reverse_lazy('cats:cats_list')

    def form_valid(self, form):
        # Сохраняем кошку без записи в БД, чтобы назначить владельца
        cat = form.save(commit=False)
        cat.owner = self.request.user
        cat.save()

        # Отправляем уведомление
        send_cat_creation(cat.owner.email, cat)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить кошку'
        return context


# 7. РЕДАКТИРОВАНИЕ КОШКИ (с проверкой прав и родословной)
class CatUpdateView(LoginRequiredMixin, UpdateView):
    model = Cat
    form_class = CatForm
    template_name = 'cats/create_update.html'
    success_url = reverse_lazy('cats:cats_list')

    # Проверка прав доступа
    def get_object(self, queryset=None):
        cat = super().get_object(queryset)
        user = self.request.user

        # Доступ разрешен только владельцу или админу/модератору
        if cat.owner != user and user.role not in ['admin', 'moderator']:
            raise Http404("У вас нет прав на редактирование этой кошки")

        return cat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаем формсет для родословной
        PedigreeFormSet = inlineformset_factory(
            Cat,
            Pedigree,
            form=PedigreeForm,
            extra=2,  # Количество пустых форм для новых родителей
            can_delete=True  # Возможность удалять существующие записи
        )

        if self.request.method == 'POST':
            context['formset'] = PedigreeFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PedigreeFormSet(instance=self.object)

        context['title'] = f'Изменить кошку {self.object.name}'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        # Сначала сохраняем основную форму (кошку)
        self.object = form.save()

        # Если формсет валиден, сохраняем родословную
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

# 8. Родословная

class PedigreeView(DetailView):
    model = Cat
    template_name = 'cats/pedigree.html'
    context_object_name = 'cat'

    def get_queryset(self):
        # Показываем родословную только активных кошек
        return Cat.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Родословная: {self.object.name}'
        return context

# 9. УДАЛЕНИЕ КОШКИ (Soft Delete + проверка прав)
"""class CatDeleteView(LoginRequiredMixin, DeleteView):
    model = Cat
    template_name = 'cats/delete.html'
    success_url = reverse_lazy('cats:cats_list')

    # Проверка прав
    def get_object(self, queryset=None):
        cat_object = super().get_object(queryset)
        if cat_object.owner != self.request.user and self.request.user.role not in ['admin', 'moderator']:
            raise Http404
        return cat_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Вы уверены, что хотите удалить кошку {self.object.name}?'
        return context
"""


class CatDeleteView(LoginRequiredMixin, View):
    template_name = 'cats/delete.html'

    def get(self, request, pk):
        """Показываем страницу подтверждения"""
        cat = get_object_or_404(Cat, pk=pk)
        # Проверка прав
        if cat.owner != request.user and request.user.role not in ['admin', 'moderator']:
            raise Http404
        return render(request, self.template_name, {
            'object': cat,
            'title': f'Вы уверены, что хотите удалить кошку {cat.name}?'
        })

    def post(self, request, pk):
        """Обрабатываем удаление (SOFT DELETE)"""
        cat = get_object_or_404(Cat, pk=pk)
        # Проверка прав
        if cat.owner != request.user and request.user.role not in ['admin', 'moderator']:
            raise Http404

        # МЕНЯЕМ СТАТУС ВМЕСТО УДАЛЕНИЯ
        cat.is_active = False
        cat.save()

        # Перенаправляем на список
        return HttpResponseRedirect(reverse_lazy('cats:cats_list'))
