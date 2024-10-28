from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, TemplateView
from taggit.models import Tag
from .forms import CommentForm, SearchForm
from .models import Post, Category
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count


def post_list(request, tag_slug=None, category_id=None):
    posts_list = Post.published.all()
    tag = None
    category = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        posts_list = posts_list.filter(category=category)

    # Get all tags associated with posts and remove duplicates
    unique_tags = Tag.objects.filter(post__in=posts_list).annotate(post_count=Count('post')).distinct()
    categories = Category.objects.all()

    paginator = Paginator(posts_list, 4)  # Adjust number of posts per page
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    template_name = 'list.html' if tag_slug or category_id else 'index.html'

    return render(request, template_name, {
        'categories': categories,
        'posts': posts,
        'tag': tag,
        'category': category,
        'unique_tags': unique_tags
    })


class PostDetailView(DetailView, FormView):
    model = Post
    template_name = 'post-detail.html'
    context_object_name = 'detail'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CommentForm'] = self.get_form()

        # Fetch the current post object
        post = self.get_object()

        # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids) \
            .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                            .order_by('-same_tags', '-publish')[:4]

        # Add similar posts to the context
        context['similar_posts'] = similar_posts

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        return super().form_valid(form)

    def get_object(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']

        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=slug,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )

    def get_success_url(self):
        return reverse_lazy('exam:post_list')


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
                rank=SearchRank(SearchVector('title', 'body'), search_query)
            ).filter(search=search_query).order_by('-rank')
    return render(request, 'list.html', {
        'form': form,
        'query': query,
        'results': results
    })


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'
