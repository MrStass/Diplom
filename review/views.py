from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Review
from main.models import Book
from .forms import ReviewForm


@login_required
@require_POST
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.save()
        average_rating = book.average_rating()
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'user': review.user.username,
                'text': review.text,
                'rating': review.rating,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'average_rating': average_rating
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book = review.book
    review.delete()
    average_rating = book.average_rating()
    return JsonResponse({
        'success': True,
        'average_rating': average_rating
    })


@login_required
@require_POST
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        form.save()
        book = review.book
        average_rating = book.average_rating()
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'updated_at': review.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            },
            'average_rating': average_rating
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)