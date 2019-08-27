from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post
from comment.commentforms import CommentForm
from comment.models import Comment, Snap
import json
# Create your views here.


class CommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    http_method_names = ['post']

    def post(self, request):
        context = {
            'succeed': False,
            'errors': None,
        }
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            reply_to_user = get_object_or_404(User, userinfo__name=comment_form.cleaned_data.get('reply_to'))
            reply_to_blog = get_object_or_404(Post, id=comment_form.cleaned_data.get('reply_to_blog'))
            parent = comment_form.cleaned_data.get('parent')
            content = comment_form.cleaned_data.get('content')
            if len(parent) > 0:
                Comment.objects.create(reply=request.user, reply_to_blog=reply_to_blog, reply_to=reply_to_user,
                                       content=content, parent_id=parent)
            else:
                Comment.objects.create(reply=request.user, reply_to_blog=reply_to_blog, reply_to=reply_to_user,
                                       content=content)
            context['succeed'] = True

        else:
            context['errors'] = comment_form.errors.as_json()
            print(comment_form.errors)

        return HttpResponse(json.dumps(context))


class SnapView(View):

    http_method_names = ['post', ]

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps("redirect"))
        msg = False
        post_id = request.POST.get('post_id')
        status = Snap.objects.filter(post_id=post_id, user=request.user)
        if status.exists():
            status.delete()
        else:
            Snap.objects.create(post_id=post_id, user=request.user)
            msg = True

        return HttpResponse(json.dumps(msg))
