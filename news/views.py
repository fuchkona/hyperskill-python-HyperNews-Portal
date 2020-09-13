import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from hypernews import settings


class NewsIndex(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('q')

        posts = sorted(get_posts(), key=lambda k: k['created'], reverse=True)

        if search:
            posts = filter(lambda post: search in post['title'], posts)

        grouped_by_date = {}

        for post in posts:
            created_at = post['created'].split(' ')[0]

            if created_at not in grouped_by_date.keys():
                grouped_by_date[created_at] = [post]
            else:
                grouped_by_date[created_at].append(post)

        return render(
            request, 'news/index.html', context={
                'search': search,
                'grouped_by_date': grouped_by_date
            }
        )


class NewsShow(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/show.html', context={
                'post': get_post(kwargs['post_id'])
            }
        )


class NewsCreate(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/create.html', context={
            }
        )

    def post(self, request, *args, **kwargs):
        post_title = request.POST.get('title')
        post_text = request.POST.get('text')
        add_post(post_title, post_text)
        return redirect('/news/')


def get_posts():
    posts_file = open(settings.NEWS_JSON_PATH, 'r')
    posts = json.load(posts_file)
    posts_file.close()
    return posts


def get_latest_post():
    posts = sorted(get_posts(), key=lambda k: k['created'])
    if len(posts):
        return posts.pop()
    return None


def get_latest_post_id():
    post = get_latest_post()
    if post:
        return int(post['link'])
    return 0


def get_post(post_id):
    posts = get_posts()
    for post in posts:
        if post['link'] == post_id:
            return post
    return None


def save_new_post(new_post):
    if new_post['link']:
        posts = get_posts()
        posts.append(new_post)
        with open(settings.NEWS_JSON_PATH, 'w') as file:
            json.dump(posts, file)


def add_post(title, text):
    if len(title) and len(text):
        new_post = {
            'title': title,
            'text': text,
            'created': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            'link': get_latest_post_id() + 1
        }
        save_new_post(new_post)
