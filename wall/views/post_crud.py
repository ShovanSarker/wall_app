from rest_framework.views import APIView
from rest_framework.response import Response

from wall.models import Writer
from wall.models import Post
from wall.models import Comment

from utility import check_params
from utility import RequestResponse


class CreatePost(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['sid', 'title', 'content']):
            post_data = request.POST
            user = Writer.get_user_by_session(post_data['sid'])
            if user is not None:
                if len(post_data['content']) <= 2048:
                    new_post = Post(writer=user,
                                    title=post_data['title'],
                                    content=post_data['content'])
                    new_post.save()
                    response.set_status(200)
                    response.set_message('Post uploaded successfully')
                else:
                    response.set_status(400)
                    response.set_message('Content too large')
            else:
                response.set_status(400)
                response.set_message('Incorrect session')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())


class ReadPost(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, []):
            post_data = request.POST
            max_per_request = 5
            first_post = 0
            if 'max_per_request' in post_data:
                try:
                    max_per_request = int(post_data['max_per_request'])
                except ValueError:
                    pass
            if 'first_post' in post_data:
                try:
                    first_post = int(post_data['first_post'])
                except ValueError:
                    pass
            data = {'next_post_serial': first_post + max_per_request}
            posts = Post.objects.filter(published=True).order_by('-created_at')[first_post:first_post +
                                                                                           max_per_request]
            selected_posts = []
            for post in posts:
                all_comments = Comment.objects.filter(published=True, post=post).order_by('created_at')
                comments = []
                for comment in all_comments:
                    one_comment = {
                        'commenter': comment.commenter.pk,
                        'commenter_username': comment.commenter.username,
                        'comment': comment.content,
                        'comment_published': comment.created_at.strftime("%A, %d. %B %Y %I:%M%p")

                    }
                    comments.append(one_comment)
                one_post = {
                    'post_id': post.id,
                    'post_title': post.title,
                    'post_content': post.content,
                    'post_published': post.created_at.strftime("%A, %d. %B %Y %I:%M%p"),
                    'post_writer': post.writer.pk,
                    'post_writer_username': post.writer.username,
                    'comments': comments
                }
                selected_posts.append(one_post)
            data['posts'] = selected_posts
            response.set_status(200)
            response.set_message('Post loaded successfully')
            response.set_data(data)
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())


class PostComment(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['sid', 'pid', 'comment']):
            post_data = request.POST
            user = Writer.get_user_by_session(post_data['sid'])
            if user is not None:
                if Post.objects.filter(pk=post_data['pid']).exists():
                    post_object = Post.objects.get(pk=post_data['pid'])
                    new_comment = Comment(post=post_object,
                                          commenter=user,
                                          content=post_data['comment'])
                    new_comment.save()
                    response.set_status(200)
                    response.set_message('Comment added successfully')
                else:
                    response.set_status(400)
                    response.set_message('Invalid post id')
            else:
                response.set_status(400)
                response.set_message('Incorrect session')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())


class DeletePost(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['sid', 'pid']):
            post_data = request.POST
            user = Writer.get_user_by_session(post_data['sid'])
            if user is not None:
                if Post.objects.filter(pk=post_data['pid']).exists():
                    post_object = Post.objects.get(pk=post_data['pid'])
                    if post_object.writer == user:
                        post_object.delete()
                        response.set_status(200)
                        response.set_message('Post uploaded successfully')
                    else:
                        response.set_status(400)
                        response.set_message('Do not have access to delete')
                else:
                    response.set_status(400)
                    response.set_message('Post not found. Invalid "pid"')
            else:
                response.set_status(400)
                response.set_message('Incorrect session')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())