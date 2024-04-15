from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms.models import model_to_dict
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import JsonResponse

from .models import Tag, Reminder
from .forms import ReminderForm
# Create your views here.

###################### TAGS ##########################

class TagListView(ListView):
    model = Tag
    
class TagDetailView(DetailView):
    model = Tag

class TagCreateView(CreateView):
    model = Tag
    fields = ['name', 'homework']

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Tag "{tag_name}" has been created'.format(
                tag_name=self.object.name))
        return response

    def get_success_url(self):
    	return reverse_lazy("reminders:tag_detail", args=[self.object.id])

class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name', 'homework']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Tag "{tag_name}" has been updated'.format(
                tag_name=self.object.name))
        return response
    
    def get_success_url(self):
        return reverse_lazy("reminders:tag_detail", args=[self.object.id])


###################### Reminders ##########################

class ReminderListView(ListView):
    model = Reminder


class ReminderDetailView(DetailView):
    model = Reminder


class ReminderCreateView(CreateView):
    model = Reminder
    form_class = ReminderForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Reminder "{reminder_name}" has been created'.format(
                reminder_name=self.object.name))
        return response
    
    # comment the following line to show the error about not having an
    # success_url
    def get_success_url(self):
        return reverse_lazy("reminders:reminder_detail", args=[self.object.id])

class ReminderUpdateView(UpdateView):
    model = Reminder
    template_name_suffix = '_edit'
    fields = ['name', 'homework', 'tags', 'description', 'date']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Reminder "{reminder_name}" has been updated'.format(
                reminder_name=self.object.name))
        return response
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       reminder_dico = model_to_dict(self.object)
       reminder_dico["date"] = reminder_dico["date"].strftime(
           "%Y-%m-%d"
       )
       tags = reminder_dico["tags"]
       reminder_tag_list = []
       for tag in tags:
           reminder_tag_list.append({"id": tag.id, "name": tag.name})
       reminder_dico["tags"] = reminder_tag_list
       tag_list = list(Tag.objects.all().values())
       context["reminder_dict"] = reminder_dico
       context["tag_list"] = tag_list
       print("context", context)
       return context
    
    # comment the following line to show the error about not having an
    # success_url
    def get_success_url(self):
        return reverse_lazy("reminders:reminder_detail", args=[self.object.id])

class ReminderDeleteView(DeleteView):
    model = Reminder
    success_url = reverse_lazy("reminders:reminder_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(
            self.request, messages.SUCCESS,
            'Reminder "{reminder_name}" has been deleted'.format(
                reminder_name=self.object.name))
        return response
    
class ReminderUpdatebisView(View):
    def post(self, request, *args, **kwargs):
       reminder = get_object_or_404(Reminder, pk=self.kwargs["pk"])
       # Create a form instance with POST data
       form = ReminderForm(request.POST, instance=reminder)
       if form.is_valid():
           form.save()
           return JsonResponse({"success": True})
       else:
           return JsonResponse({"success": False, "errors": form.errors})
    
class ReminderDetailbisView(TemplateView):
    template_name = "reminders/reminder_detailbis.html"
    def get(self, request, *args, **kwargs):
        reminder = get_object_or_404(Reminder, pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reminder_id'] = self.kwargs["pk"]
        return context
    
class ReminderDetailJsView(View):
    def get(self, request, *args, **kwargs):
        reminder = get_object_or_404(Reminder, pk=self.kwargs["pk"])
        reminder_js = model_to_dict(reminder)
        reminder_js["tags"] = []
        for tag in reminder.tags.values():
            reminder_js["tags"].append(tag)
        return JsonResponse({"reminder": reminder_js})

