from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# def post_list(request):
#     # пагинация
#     paginator = Paginator(posts_list, 3)
#     page_number = request.GET.get('page', 1)
#
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    return render(request, 'blog/post/detail.html', {'post': get_object_or_404(Post,
                                                                               slug=post,
                                                                               publish__year=year,
                                                                               publish__month=month,
                                                                               publish__day=day,
                                                                               status=Post.Status.PUBLISHED)})


def post_share(request, post_id):
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form,
                                                    'post': get_object_or_404(Post,
                                                                              id=post_id,
                                                                              status=Post.Status.PUBLISHED)})
