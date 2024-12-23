from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import News, Category
from .forms import ContactForm
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView


def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'news/news_list.html', context)

""" News Detail Page """
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }
    return render(request, 'news/news_detail.html', context)

# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'
#     def get_context_data(self, news, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['news'] = get_object_or_404(News, slug=news, status=News.Status.Published)
#
#         return context

""" Home Page View """
''' # Funksiya yordamida'''
# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-published_time')[:5]
#
#     # Mahalliy yangiliklar
#     mahalliy_news_1 = News.objects.filter(category__name='Mahalliy').order_by('-published_time')[0:1]
#     mahalliy_news_list = News.objects.all().filter(category__name='Mahalliy').order_by('-published_time')[1:6]
#
#     # Xorijiy yangiliklar
#     xorij_news_1 = News.objects.filter(category__name='Xorij').order_by('-published_time')[0:1]
#     xorij_news_list = News.objects.all().filter(category__name='Xorij').order_by('-published_time')[1:6]
#
#     # Texnalogiya yangiliklari
#     texno_news_1 = News.objects.filter(category__name='Texnalogiya').order_by('-published_time')[0:1]
#     texno_news_list = News.objects.all().filter(category__name='Texnalogiya').order_by('-published_time')[1:6]
#
#     # Avto yangiliklar
#     avto_news_1 = News.objects.filter(category__name="Avto").order_by('-published_time')[0:1]
#     avto_news_list = News.objects.all().filter(category__name="Avto").order_by('-published_time')[1:6]
#
#     # Sport yangiliklar
#     sport_news_list = News.objects.filter(category__name="Sport").order_by('-published_time')[:6]
#
#     context = {
#         "news_list": news_list,
#         "categories": categories,
#         "mahalliy_news_1": mahalliy_news_1,
#         "mahalliy_news_list": mahalliy_news_list,
#         "xorij_news_1": xorij_news_1,
#         "xorij_news_list": xorij_news_list,
#         "texno_news_1": texno_news_1,
#         "texno_news_list": texno_news_list,
#         "avto_news_1": avto_news_1,
#         "avto_news_list": avto_news_list,
#         "sport_news_list": sport_news_list,
#     }
#
#     return render(request, 'news/home.html', context)

''' # class yordamida '''
class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:5]
        context['mahalliy_news_list'] = News.published.all().filter(category__name='Mahalliy').order_by('-published_time')[:6]
        context['xorij_news_list'] = News.published.all().filter(category__name='Xorij').order_by('-published_time')[:6]
        context['texno_news_list'] = News.published.all().filter(category__name='Texnalogiya').order_by('-published_time')[:6]
        context['avto_news_list'] = News.published.all().filter(category__name="Avto").order_by('-published_time')[:6]
        context['sport_news_list'] = News.published.all().filter(category__name="Sport").order_by('-published_time')[:6]

        return context


''' Contact View '''
# def contactPageView(request):
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bo'langanligingiz uchun rahmat!</h1>")
#     context = { "form": form }
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langanligingiz uchun rahmat!</h1>")
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

class MahalliyNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy').order_by('-published_time')
        return news


class XorijNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorijiy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news

class TexnoNewsView(ListView):
    model = News
    template_name = 'news/texnalogiya.html'
    context_object_name = 'texno_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnalogiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news


class AvtoNewsView(ListView):
    model = News
    template_name = 'news/avto.html'
    context_object_name = 'avto_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Avto')
        return news

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image','category', 'status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('homepage')

class NewsCreateView(CreateView):
    model = News
    fields = ('title','slug', 'body', 'image','category', 'status')
    template_name = 'crud/news_create.html'
