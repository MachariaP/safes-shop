from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.contrib import messages
from store.models import Order, OrderItem
from .models import TeamMember, Solution, Testimonial, Profile


class AboutUsView(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'core/contact.html'


class SolutionsView(TemplateView):
    template_name = 'core/solutions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solutions'] = Solution.objects.all()
        context['testimonials'] = Testimonial.objects.all()
        return context


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'core/account.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        # Update user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)

        # Get orders with prefetched items
        orders = Order.objects.filter(user=user).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related(
                'product'))
        ).order_by('-created_at')

        context.update({
            'user': user,
            'profile': profile,
            'orders': orders,
            'active_tab': self.request.GET.get('tab', 'profile')
        })
        return context
