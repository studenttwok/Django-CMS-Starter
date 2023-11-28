from typing import Any
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.timezone import now
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Page, Image, Tag, ArticleCategory, Album, AlbumImage, Profile
from cms_starter.utils import to_slug

admin.site.site_header = "CMS Site Admin"
admin.site.site_title = "CMS Admin Portal"
admin.site.index_title = "Dashboard"


class PageImagesInLine(admin.StackedInline):
    model = Page.images.through
    extra = 0
    autocomplete_fields = ["image"]
class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content': CKEditorUploadingWidget(),
        }

class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'parent_page', 'published')
    inlines = (PageImagesInLine,)
    list_filter = ('published','parent_page')
    exclude = ('created_by', 'created_at', 'modified_at')
    search_fields = ('title',)
    def save_model(self, request, obj, form, change):
        if obj.slug is None or obj.slug == "":
            obj.slug = to_slug(obj.title)
        super().save_model(request, obj, form, change)

class ArticleCategoriesInLine(admin.StackedInline):
    model = Article.categories.through
    extra = 0
class ArticleImagesInLine(admin.StackedInline):
    model = Article.images.through
    autocomplete_fields = ["image"]
    extra = 0
    

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'summary': CKEditorWidget(),
            'content': CKEditorUploadingWidget(),
        }
class ArticleTagInLine(admin.StackedInline):
    model = Article.tags.through
    extra = 0
    autocomplete_fields = ["tag"]

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'created_by', 'published', 'modified_at')
    inlines = (ArticleCategoriesInLine, ArticleImagesInLine, ArticleTagInLine)
    list_filter = ('published', 'created_by')
    search_fields = ('title', 'summary', 'content', 'bgg_id')
    exclude = ('created_by', 'created_at', 'modified_at')

    search_fields = ["tags"]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.modified_at = now()
        if obj.slug is None or obj.slug == "":
            obj.slug = to_slug(obj.title)
        super().save_model(request, obj, form, change)
    

class ImageArticleInLine(admin.TabularInline):
    model = Image.articles.through
    autocomplete_fields = ["article"]
    extra = 0
class ImagePageInLine(admin.TabularInline):
    model = Image.pages.through
    autocomplete_fields = ["page"]
    extra = 0
class ImageAlbumImageInLine(admin.StackedInline):
    model = AlbumImage
    autocomplete_fields = ["album", "image"]
    extra = 0
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'caption', 'published')
    list_filter = ( 'pages',)
    search_fields = ('caption', 'articles__title', 'pages__title')
    inlines = (ImageAlbumImageInLine, ImageArticleInLine, ImagePageInLine,)
    fields = ('image', 'image_tag', 'caption', 'published')
    readonly_fields = ('image_tag',)


class ArticleCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = '__all__'
        widgets = {
            'description': CKEditorUploadingWidget(),
        }
class ArticleCategoryAdmin(admin.ModelAdmin):
    form = ArticleCategoryAdminForm
    prepopulated_fields = {'slug': ('name',)}
    def save_model(self, request, obj, form, change):
        if obj.slug is None or obj.slug == "":
            obj.slug = to_slug(obj.name)
        super().save_model(request, obj, form, change)

class TagArticlesInLine(admin.TabularInline):
    model = Tag.articles.through
    autocomplete_fields = ["article"]
    extra = 0
    
class TagAdmin(admin.ModelAdmin):
    def article_count(self, obj):
        return obj.articles.count()
    list_display = ('name', 'article_count')
    search_fields = ('name',)
    inlines = (TagArticlesInLine,)
    fields = ('name',)



class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
        widgets = {
            'short_description': CKEditorWidget(),
            'description': CKEditorUploadingWidget(),
        }

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumAdminForm
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'published')
    list_filter = ('published',)
    search_fields = ('name', 'description')
    inlines = (ImageAlbumImageInLine,)
    exclude = ('created_by', 'created_at', 'modified_at')
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        if obj.slug is None or obj.slug == "":
            obj.slug = to_slug(obj.name)
        super().save_model(request, obj, form, change)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'
    
class UserWithProfileAdmin(UserAdmin):
    def profile(self, obj):
        return obj.profile
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    inlines = (ProfileInline,)

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'bio': CKEditorWidget(),
        }
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    exclude = ('user', 'created_by', 'created_at', 'modified_at')
    form = ProfileAdminForm

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # only show profiles for the logged in user if the user is not a superuser
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        # onmly save if the user is the same as the logged in user
        if request.user.is_superuser or obj.user == request.user:
            obj.created_by = request.user
            super().save_model(request, obj, form, change)

admin.site.register(Page, PageAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(User)
admin.site.register(User, UserWithProfileAdmin)
admin.site.register(Profile, ProfileAdmin)

