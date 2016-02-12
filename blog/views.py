from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
#class view
#from django.views.generic import ListView
from taggit.models import Tag

from .models import Post

# Create your views here.
'''
class PostListView(ListView):
	queryset = Post.published.all()
	
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'
'''


def post_list(request, tag_slug=None):
	
	object_list = Post.published.all()
	tag = None
	
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag] )
		
		
	paginator = Paginator(object_list, 3) # 3posts
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	
	return render(request, 'blog/post/list.html', {'page': page, 'posts':posts, 'tag': tag } )



def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
	
	#list similar posts
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]									
	
	return render(request,'blog/post/detail.html', {'post':post, 'similar_posts':similar_posts})
	