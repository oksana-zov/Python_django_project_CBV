from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm
from .utils import generate_slug
from users.models import UserRoles
from django.db.models import Q
from django.http import Http404
from reviews.services import censor_text
from django.contrib import messages


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews_list'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(sign_of_review=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отзывы о кошках'
        return context


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews_list'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset().filter(sign_of_review=False)
        # Админ видит все, модератор и автор - только свои/на модерации
        user = self.request.user
        if user.role == UserRoles.ADMIN:
            return qs
        return qs.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отзывы на модерации'
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        if self.request.user.role not in (UserRoles.USER, UserRoles.ADMIN, UserRoles.MODERATOR):
            return HttpResponseForbidden()

        review = form.save(commit=False)

        # БЛОК ЦЕНЗУРЫ
        original_text = form.cleaned_data.get('content', '')
        _, has_bad_words = censor_text(original_text)

        # Если есть плохие слова — блокируем сохранение
        if has_bad_words:
            form.add_error('content',
                           'Ваш отзыв содержит недопустимые слова. Пожалуйста, удалите их или замените на корректные.')
            return self.form_invalid(form)

        # Если всё чисто — сохраняем
        review = form.save(commit=False)
        review.sign_of_review = False

        if review.slug == 'temp_slug':
            review.slug = generate_slug()
        review.author = self.request.user
        review.save()
        return redirect(review.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Написать отзыв'
        return context


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        if review.author != self.request.user:
            raise Http404()
        return review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать отзыв: {self.object.title}'
        return context


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    permission_required = 'reviews.delete_review'
    success_url = reverse_lazy('reviews:reviews_list')


# ПОИСК ПО ОТЗЫВАМ
class ReviewSearchListView(ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews_list'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            # Ищем по заголовку ИЛИ тексту отзыва, только опубликованные
            return Review.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                sign_of_review=True
            )
        return Review.objects.filter(sign_of_review=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска отзывов: "{self.request.GET.get("q", "")}"'
        context['search_query'] = self.request.GET.get('q', '')
        return context


def review_toggle_activity(request, slug):
    review = get_object_or_404(Review, slug=slug)
    if not request.user.is_authenticated or request.user.role not in ('admin', 'moderator'):
        raise Http404()

    review.sign_of_review = not review.sign_of_review
    review.save()

    if review.sign_of_review:
        return redirect('reviews:reviews_list')
    return redirect('reviews:reviews_deactivated')
