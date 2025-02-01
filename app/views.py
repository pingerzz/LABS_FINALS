from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import LostAndFoundItem
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LostAndFoundItem, Category
from django.db import models



from django.contrib.auth.decorators import login_required

class HomePageView(TemplateView):
    template_name = 'app/home.html'

class AboutPageView(TemplateView):
    template_name = 'app/about.html'

class LostItemList(LoginRequiredMixin, ListView):
    model = LostAndFoundItem
    context_object_name = 'lostitem'
    template_name = 'app/lostitemlist.html'

    def get_queryset(self):
        # Get only items marked as "Lost"
        return LostAndFoundItem.objects.filter(status='lost')

    def dispatch(self, request, *args, **kwargs):
        # If the user is not authenticated, redirect to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Initial queryset for items marked as 'lost'
        queryset = LostAndFoundItem.objects.filter(status='lost')

        # Process search query (q)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(item__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(location__icontains=query) |
                models.Q(contact_name__icontains=query)
            )

        # Process category filter (if selected)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Process sorting option (default: '-date' for newest items first)
        sort_by = self.request.GET.get('sort', '-date')
        queryset = queryset.order_by(sort_by)

        return queryset  # Return only filtered and sorted data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Add categories for dropdown filter
        return context




class LostItemView(LoginRequiredMixin, DetailView):
    model = LostAndFoundItem
    context_object_name = 'lostitem'
    template_name = 'app/lostitemdetail.html'


class AddLostItem(LoginRequiredMixin, CreateView):
    model = LostAndFoundItem
    fields = ['item','description','category','status','location','date','contact_name','contact_phone','image']
    template_name = 'app/addlostitem.html'

class UpdateLostItem(LoginRequiredMixin, UpdateView):
    model = LostAndFoundItem
    fields = ['item','description','category','status','location','date','contact_name','contact_phone','image']
    template_name = 'app/updatelostitem.html'

class DeleteLostItem(LoginRequiredMixin, DeleteView):
    model = LostAndFoundItem
    template_name = 'app/deletelostitem.html'
    success_url = reverse_lazy('lost-item')

class LoginPageView(TemplateView):
    template_name = 'app/templates/registration/login.html'

class SignupPageView(TemplateView):
    template_name = 'app/templates/registration/signup.html'

class ReportPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/reports.html'

    def dispatch(self, request, *args, **kwargs):
        # If the user is not authenticated, redirect to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)




class ItemPageView(LoginRequiredMixin, TemplateView):
    model = LostAndFoundItem
    context_object_name = 'lostitem'
    template_name = 'app/item.html'

class FoundItemPageView(LoginRequiredMixin, ListView):
    model = LostAndFoundItem
    context_object_name = 'founditems'  # This must match what the template uses
    template_name = 'app/founditem.html'  # Ensures this template is used

    def get_queryset(self):
        # Filter only items with status='found'
        return LostAndFoundItem.objects.filter(status__iexact='found')

    def dispatch(self, request, *args, **kwargs):
        # If the user is not authenticated, redirect to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Queryset for items with status="found"
        queryset = LostAndFoundItem.objects.filter(status__iexact='found')

        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(item__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(location__icontains=query) |
                models.Q(contact_name__icontains=query)
            )

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)

        # Sorting options
        sort_by = self.request.GET.get('sort', '-date')  # Sort by newest items first by default
        queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass categories to template for filtering
        return context





def update_status_to_found(request, pk):
    # Get the lost item or return a 404 error if it doesn't exist
    lost_item = get_object_or_404(LostAndFoundItem, pk=pk)

    # Check if the item is "Lost" before changing it to "Found"
    if lost_item.status == 'lost':
        # Update the status to "Found"
        lost_item.status = 'Found'
        lost_item.save()  # Save the change

    # Redirect to the "Found Items" page
    return redirect('found-item')

class LogOutPageView(TemplateView):
    template_name = 'app/logout page.html'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
