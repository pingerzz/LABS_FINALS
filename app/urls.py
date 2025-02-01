from django.urls import path
from django.contrib.auth.views import LoginView
from .views import HomePageView, AboutPageView, AddLostItem, LostItemView, LostItemList, UpdateLostItem, DeleteLostItem, LoginPageView, SignupPageView, ReportPageView, ItemPageView, update_status_to_found, FoundItemPageView, LogOutPageView, CustomLoginView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('lost-item/', LostItemList.as_view(), name='lost-item'),
    path('lost-item/<int:pk>/', LostItemView.as_view(), name='lost-item-view'),
    path('lost-item/add', AddLostItem.as_view(), name='add-lost-item'),
    path('lost-item/<int:pk>/update', UpdateLostItem.as_view(), name='update-lost-item'),
    path('lost-item/<int:pk>/delete', DeleteLostItem.as_view(), name='delete-lost-item'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('reports/', ReportPageView.as_view(), name='reports'),
    path('item/', ItemPageView.as_view(), name='item'),
    path('update-status-to-found/<int:pk>/', update_status_to_found, name='update-status-to-found'),  # Only one path for this
    path('found-item/', FoundItemPageView.as_view(), name='found-item'),

    path('log-out/', LogOutPageView.as_view(), name='log-out'),

    path('login/', CustomLoginView.as_view(), name='login'),

]
