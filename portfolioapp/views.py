from django.shortcuts import get_object_or_404

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.utils.views import render

def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html"):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    blog_posts = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    cats = blog_post.categories.all()
    if cats.exists():
        cat_slug = cats[0].slug
    context = {"blog_post": blog_post, "editable_obj": blog_post}
    templates = [u"blog/blog_post_detail_%s.html" % unicode(cat_slug), u"blog/blog_post_detail_%s.html" % unicode(slug), template]
    return render(request, templates, context)
