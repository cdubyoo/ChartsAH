from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Post
# Create your views here.


class CommentNoticeListView(LoginRequiredMixin, ListView):
    context_object_name = 'comment_notices'
    template_name = 'notice/list.html'


    # get qs of unread notifications
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    def get(self, request):
        notice_id = request.GET.get('notice_id') #getting notice_id from html name

        if notice_id: #if html element has notice_id 
            request.user.notifications.get(id=notice_id).mark_as_read() #delete the notification using its value called in template
            return redirect('notice:list')

        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')


