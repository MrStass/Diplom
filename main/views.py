from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, View
from main.forms import BookVectorForm, BookSelectForm
from main.models import *
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from cart.models import *
import pickle
from django.views.generic.edit import FormMixin
from django.urls import reverse
from review.forms import ReviewForm
from django.http import HttpResponseRedirect


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Book
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            # Отримуємо кошик користувача, якщо існує
            cart, created = Cart.objects.get_or_create(user=user)
            # Отримуємо список ID книг в кошику
            cart_books_ids = cart.items.values_list('book__id', flat=True)
            context['cart_books_ids'] = cart_books_ids

            recommendation = RecommendedBook.objects.filter(user=user).first()
            if recommendation:
                context['recommended_books'] = recommendation.recommended.all()
        return context

class ChooseGenre(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        genre_id = self.kwargs.get('genre_id')
        return Book.objects.filter(genres__id=genre_id)


class BookDetailView(FormMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = ReviewForm
    context_object_name = 'book'

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.book = self.object
        review.user = self.request.user
        review.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['reviews'] = self.object.reviews.all()
        return context


vectorizer_path = '/app/resources/vectorizer.pkl'


class BookVectorView(FormView):
    template_name = 'vector.html'
    form_class = BookVectorForm
    success_url = reverse_lazy('vectorize_book')

    def form_valid(self, form):
        # Завантаження збереженого векторизатора
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)

        book = form.cleaned_data['book']
        description = form.cleaned_data['description']

        # Використання існуючого векторизатора для трансформації опису
        vector = vectorizer.transform([description]).toarray()
        serialized_vector = pickle.dumps(vector)

        BookVector.objects.update_or_create(
            book=book,
            defaults={'vector': serialized_vector}
        )

        return super().form_valid(form)


class VectorDisplayView(View):
    form_class = BookSelectForm
    template_name = 'vector_display.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            book_vector_instance = BookVector.objects.get(book=book)
            vector_data = pickle.loads(book_vector_instance.vector)

            vector_data_list = vector_data.tolist()

            return render(request, self.template_name, {
                'form': form,
                'vector_data': vector_data_list,
                'selected_book': book
            })
        return render(request, self.template_name, {'form': form})


class SearchView():
    template_name = 'index.html'
    model = Book
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query))
        return super(SearchView, self).get_queryset()
