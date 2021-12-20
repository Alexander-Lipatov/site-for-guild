from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django import views


from users.models import User, Country
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin


class ContactListView(ListView):
    model = User

    template_name = 'main_info/list_views.html'


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        if not request.user.guild_member:
            self.template_name = 'main_info/on_check.html'
        return super(ContactListView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def notifications(user):
        if user.is_authenticated:
            return Notification.objects.all(recipient=user)
        return Notification.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = self.notifications(self.request.user)
        context['posts'] = User.objects.filter(guild_member=True)

        return context


class ClearNotificationsView(views.View):
    @staticmethod
    def get(request, *args, **kwargs):
        Notification.objects.make_all_read(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class AddMemberNotificationsView(views.View):
    @staticmethod
    def get(request, pk, *args, **kwargs):
        Notification.objects.added_guild_member(pk)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DelMemberNotificationsView(views.View):
    @staticmethod
    def get(request, pk, *args, **kwargs):
        Notification.objects.del_guild_member(pk)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DynamicPostsLoad(View):

    @staticmethod
    def get(request, *args, **kwargs):
        post_id = request.GET.get('postId')
        more_info = User.objects.filter(pk=int(post_id)).values('id', 'game_nick', 'tel', 'whatsapp_boolean',
                                                                'telegram_name', 'telegram_boolean', 'viber_boolean')
        data = []
        for post in more_info:
            obj = {
                'id': post['id'],
                'game_nick': post['game_nick'],
                'tel': post['tel'],
                'is_whatsapp': post['whatsapp_boolean'],
                'is_telegram': post['telegram_boolean'],
                'is_viber': post['viber_boolean'],
                'telegram_name': post['telegram_name'],

            }
            print(obj)
            data.append(obj)
        return JsonResponse({'data': data})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        return super().dispatch(request, *args, **kwargs)
