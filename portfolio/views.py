from django.shortcuts import render
from .models import *
from .constants import Constant


def home_page(request):
    all_sections = Section.objects.all().order_by("order")
    sections = all_sections.filter(home=True)
    menu = all_sections.filter(menu=True)

    social_media = SocialMedia.objects.all()
    for section in sections:
        section.get_data()

    context = {
        "title": Constant.CONSTANT_TITLE,
        "sections": sections,
        'menu': menu,
        "social_media": social_media,
    }
    template = "portfolio/home_page.html"

    return render(request, template, context)


def link_view(request, link_name):
    page = Page.objects.filter(name=Page.url_to_name(link_name)).first()
    if page:
        page.get_data()
    context = {"title": Constant.CONSTANT_TITLE,
               'page': page}
    template = "portfolio/page.html"
    return render(request, template, context)


def handler_error(request):
    return render(request, 'portfolio/error.html')

