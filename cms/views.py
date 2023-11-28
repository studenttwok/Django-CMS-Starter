from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Page, Article, ArticleCategory, Tag, Album
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

ITEM_PER_PAGE = settings.ITEM_PER_PAGE

def index(request):
    url = reverse("page", kwargs={"slug": "home"})
    return redirect(url)

def page(request, slug):
    if request.method == 'GET':
        #page = get_object_or_404(Page, slug=slug)
        page = Page.objects.filter(slug=slug).first()
        if page is not None:
            if  page.published == True:
                return render(request, 'page.html', {'object': page})
    return render(request, '404.html', status=404)

def articles(request):
    if request.method == 'GET':
        q = request.GET.get('q') or ""
        writer = request.GET.get('writer') or ""
        category_slug = request.GET.get('category') or ""
        tag = request.GET.get('tag') or ""
        object_list = []
        category = None

        conditions = Q(published__exact=True)
        if q != "":
            conditions = conditions & (Q(title__icontains = q) | Q(content__icontains = q) | Q(slug__icontains = q))
        if writer != "":
            conditions = conditions & Q(created_by__profile__nickname__exact = writer)
        if category_slug != "":
            conditions = conditions & Q(categories__slug__exact = category_slug)
        if tag != "":
            conditions = conditions & Q(tags__name__exact = tag)


        object_list = Article.objects.filter(conditions).order_by('-created_at').select_related('created_by__profile').all()

        if object_list is not None:

            paginator = Paginator(object_list, ITEM_PER_PAGE) # Show ITEM_PER_PAGE contacts per page.
            page_number = request.GET.get('page') or 1
            page_obj = paginator.get_page(page_number)
            num_of_articles = page_obj.object_list.count

            # if it is article
            # also query the ArticleCategory and tags
            all_articlecategories = ArticleCategory.objects.annotate(article_count=Count('articles__id', filter=Q(articles__published__exact = True))).order_by('name').all()
            all_tags = Tag.objects.annotate(article_count=Count('articles__id', filter=Q(articles__published__exact = True))).order_by('-article_count')

            # if category is not empty, then get the category object
            
            if category_slug != "":
                category = get_object_or_404(ArticleCategory, slug=category_slug)
            
            return render(request, 'articles.html', {
                'object_list': page_obj, 
                'page_number': page_number, 
                'total_page_number': paginator.num_pages, 
                'q': q, 
                'writer': writer,
                'articlecategory': category,
                'tag': tag,
                'all_articlecategories': all_articlecategories, 
                'all_tags': all_tags,
                'num_of_articles': num_of_articles,
                })
        else:
            return render(request, '404.html', status=404)
    return render(request, '404.html', status=404)        


def article(request, id, slug):
    if request.method == 'GET':
        # content_type = request.GET.get('content_type')
        object = get_object_or_404(Article, id=id)
        # only show published content
        if not object.published:
            return render(request, '404.html', status=404)

        # get tags
        tags = object.tags.all()
        return render(request, 'article.html', {'object': object, 'tags': tags})
    return render(request, '404.html', status=404)

def albums(request):
    if request.method == 'GET':
        object_list = []

        conditions = Q(published__exact=True)
        object_list = Album.objects.filter(conditions).order_by('-id').select_related('created_by__profile').all()

        if object_list is not None:

            paginator = Paginator(object_list, ITEM_PER_PAGE) # Show ITEM_PER_PAGE contacts per page.
            page_number = request.GET.get('page') or 1
            page_obj = paginator.get_page(page_number)

            num_of_albums = page_obj.object_list.count

            return render(request, 'albums.html', {
                'object_list': page_obj, 
                'page_number': page_number, 
                'total_page_number': paginator.num_pages, 
                'num_of_albums': num_of_albums,
            })
        else:
            return render(request, '404.html', status=404)
    return render(request, '404.html', status=404)        

def album(request, id, slug):
    if request.method == 'GET':
        # content_type = request.GET.get('content_type')
        object = get_object_or_404(Album, id=id)
        # only show published content
        if not object.published:
            return render(request, '404.html', status=404)

        return render(request, 'album.html', {'object': object})
    return render(request, '404.html', status=404)        

def writers(request):
    if request.method == 'GET':
        object_list = User.objects.filter(groups__name='writer').order_by('username').select_related('profile').all()

        if object_list is not None:
            paginator = Paginator(object_list, ITEM_PER_PAGE) # Show ITEM_PER_PAGE contacts per page.
            page_number = request.GET.get('page') or 1
            page_obj = paginator.get_page(page_number)

            num_of_writers = page_obj.object_list.count

        return render(request, 'writers.html', {'object_list': page_obj, 'page_number': page_number, 'total_page_number': paginator.num_pages, 'num_of_writers': num_of_writers})
    
    return render(request, '404.html', status=404)

def writer(request, id, nickname):
    if request.method == 'GET':
        user = get_object_or_404(User, id=id)
        # only show published content
        if not user.groups.filter(name='writer').exists():
            return render(request, '404.html', status=404)

        return render(request, 'writer.html', {'object': user})
    return render(request, '404.html', status=404)
