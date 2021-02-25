from django.contrib import admin

from .models import (
    Article,
    Author,
    Category,
    Gallery,
    MetaTags,
    Step,
    StepTag,
    Tag,
    Video,
)


class MetaTagsInline(admin.TabularInline):
    model = MetaTags


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    inlines = [MetaTagsInline, GalleryInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["user"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(StepTag)
class StepTagAdmin(admin.ModelAdmin):
    list_display = ["title"]
