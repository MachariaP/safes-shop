from django.views.generic import TemplateView
from .models import TeamMember, Solution, Testimonial

# Create your views here.
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