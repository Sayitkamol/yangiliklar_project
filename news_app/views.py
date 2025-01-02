from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model

from config.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category
from .forms import ContactForm, CommentForm
from hitcount.views import HitCountDetailView, HitCountMixin


def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'news/news_list.html', context)

""" News Detail Page """


class PostCountHitDetailView(HitCountDetailView):
    model = News        # your model goes here
    count_hit = True    # set to True if you want it to try and count the hit

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request,hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    # Camment
    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None 
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekin DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # Izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # DB ga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        'comments': comments,
        'comments_count': comments_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    http_method_names = ['get', 'post']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object
        comments = news.comments.filter(active=True)
        new_comment = None

        if self.request.method == "POST":
            comment_form = CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.news = news
                new_comment.user = self.request.user
                new_comment.save()
                comment_form = CommentForm()
        else:
            comment_form = CommentForm()

        context['comments'] = comments
        context['new_comment'] = new_comment
        context['comment_form'] = comment_form
        return context


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

class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image','category', 'status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('homepage')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = ('title', 'title_uz', 'title_en', 'title_ru', 'slug', 'body', 'body_uz', 'body_en', 'body_ru', 'image','category', 'status')
    template_name = 'crud/news_create.html'
    success_url = reverse_lazy('home_page')

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users,
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query)|Q(body__icontains=query))
