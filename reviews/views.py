from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from .models import Review
from .forms import ReviewForm
from .utils import generate_slug
from users.models import UserRoles


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/reviews_list.html'
    context_object_name = 'reviews_list'

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
        context['title'] = self.review.title
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_object(self, queryset=None):
        review = super().get_object(queryset)
        if review.author != self.request.user and self.request.user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR):
            from django.http import Http404
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


def review_toggle_activity(request, slug):
    review = get_object_or_404(Review, slug=slug)
    if request.user.role not in (UserRoles.ADMIN, UserRoles.MODERATOR):
        from django.http import Http404
        raise Http404()

    review.sign_of_review = not review.sign_of_review
    review.save()

    if review.sign_of_review:
        return redirect('reviews:reviews_list')
    return redirect('reviews:reviews_deactivated')
