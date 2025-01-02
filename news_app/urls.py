from django.urls import path
from .views import (news_list, news_detail, ContactPageView, HomePageView,NewsDetailView,
                    MahalliyNewsView, XorijNewsView, TexnoNewsView, SportNewsView, AvtoNewsView,
                    NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view,
                    SearchResultsListView,
    # homePageView, contactPageView,
                    )

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('all/', news_list, name='all_news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),

    path('<slug>/edit/', NewsUpdateView.as_view(), name='news_update_page' ),
    path('<slug>/delete/', NewsDeleteView.as_view(), name='news_delete_page'),

    path('create/', NewsCreateView.as_view(), name='news_create_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('mahalliy/', MahalliyNewsView.as_view(), name='mahalliy_news_page'),
    path('xorij/', XorijNewsView.as_view(), name='xorij_news_page'),
    path('texno/', TexnoNewsView.as_view(), name='texno_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('avto/', AvtoNewsView.as_view(), name='avto_news_page'),
    path('admin_page/', admin_page_view, name='admin_page'),
    path('search/', SearchResultsListView.as_view(), name='search_page'),
]