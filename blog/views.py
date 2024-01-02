from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
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
    # извлечь пост по идентификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommend you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n {cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'stalk200213@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})
