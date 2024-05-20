from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, View
from main.forms import BookVectorForm, BookSelectForm, SearchForm
from main.models import *
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from cart.models import *
import pickle
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from review.forms import ReviewForm
from review.models import Review


class IndexView(ListView):
    template_name = 'index.html'
    model = Book
    paginate_by = 10
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart_books_ids = cart.items.values_list('book__id', flat=True)
            favorite_books_ids = Favorite.objects.filter(user=user).values_list('book__id', flat=True)

            context['cart_books_ids'] = cart_books_ids
            context['favorite_books_ids'] = favorite_books_ids

            recommendation = RecommendedBook.objects.filter(user=user).first()
            if recommendation:
                context['recommended_books'] = recommendation.recommended.all()
            else:
                context['recommended_books'] = None

        context['new_arrivals'] = Book.objects.filter(is_available=True).order_by('-created_at')[:5]
        return context


class ChooseGenre(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        genre_id = self.kwargs.get('genre_id')
        return Book.objects.filter(genres__id=genre_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart_books_ids = cart.items.values_list('book__id', flat=True)
            favorite_books_ids = Favorite.objects.filter(user=user).values_list('book__id', flat=True)

            context['cart_books_ids'] = cart_books_ids
            context['favorite_books_ids'] = favorite_books_ids

        return context


class ChooseAuthor(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        return Book.objects.filter(author__id=author_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            cart_books_ids = cart.items.values_list('book__id', flat=True)
            favorite_books_ids = Favorite.objects.filter(user=user).values_list('book__id', flat=True)

            context['cart_books_ids'] = cart_books_ids
            context['favorite_books_ids'] = favorite_books_ids

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        book = context['book']

        # Перевірка на улюблені книги
        if user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(user=user, book=book).exists()
            cart_items = CartItem.objects.filter(cart__user=user, book=book)
            context['is_in_cart'] = cart_items.exists()

        # Додавання форми для відгуків
        context['review_form'] = ReviewForm()

        # Додавання списку відгуків
        context['reviews'] = Review.objects.filter(book=book).order_by('-created_at')

        return context


vectorizer_path = '/app/resources/vectorizer.pkl'


class BookVectorView(FormView):
    template_name = 'vector.html'
    form_class = BookVectorForm
    success_url = reverse_lazy('vectorize_book')

    def form_valid(self, form):

        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)

        book = form.cleaned_data['book']
        description = form.cleaned_data['description']

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


class BookSearchView(ListView):
    model = Book
    template_name = 'search.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['search_form'] = SearchForm(self.request.GET or None)
        if user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=user).values_list('book_id', flat=True)
            context['cart_books_ids'] = set(cart_items)
            favorite_items = Favorite.objects.filter(user=user).values_list('book_id', flat=True)
            context['favorite_books_ids'] = set(favorite_items)
        else:
            context['cart_books_ids'] = set()
            context['favorite_books_ids'] = set()
        return context


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        favorite_qs = Favorite.objects.filter(user=request.user, book=book)

        if favorite_qs.exists():
            favorite_qs.delete()
            action = 'remove'
        else:
            Favorite.objects.create(user=request.user, book=book)
            action = 'add'

        return JsonResponse({'status': 'success', 'action': action})
