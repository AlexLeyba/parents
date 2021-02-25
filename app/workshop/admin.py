from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import (
    Book,
    Comment,
    Day,
    Film,
    Image,
    Info,
    Methodology,
    PartOfDay,
    Video,
    Workshop,
)


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ["title"]


class MethodologyInlines(NestedStackedInline):
    model = Methodology
    extra = 1


class FilmInlines(NestedStackedInline):
    model = Film
    extra = 1


class BookInlines(NestedStackedInline):
    model = Book
    extra = 1


class VideoInline(NestedStackedInline):
    model = Video
    extra = 1


class ImageInline(NestedStackedInline):
    model = Image
    extra = 1


class PartOfDayInline(NestedStackedInline):
    model = PartOfDay
    extra = 1
    inlines = [ImageInline]


@admin.register(Day)
class DayAdmin(NestedModelAdmin):
    list_display = ["title", "workshop"]
    inlines = [
        PartOfDayInline,
        MethodologyInlines,
        FilmInlines,
        BookInlines,
    ]


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    pass
