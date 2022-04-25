from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
import json

from .signals import media_saved, post_saved
from .serializers import *
from .forms import *

from firebaseConfig import storage as firebaseStorage


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channels(request):
    channel_list = UserProfile.objects.get(pk=request.user.pk).channel_set.filter(is_active=True)
    serializer = ChannelListSerializer(channel_list, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_details(request, channel_name):
    try:
        data = Channel.objects.get(name=channel_name)
    except Channel.DoesNotExist:
        return Response({'msg': 'Channel does not exist'}, status=404)

    serializer = ChannelDetailsSerializer(data)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts(request, last_post):
    channel = list(UserProfile.objects.get(pk=request.user.pk).channel_set.all().values_list('id'))
    posts = Post.objects.filter(posted_in__in=channel, is_hidden=False, id__lt=last_post).order_by('-pk').distinct()[:10]
    serializer = PostSerializer(posts, many=True)

    index = posts.count()

    if index < 0:
        data = {
            "msg": "No posts found.",
        }
        return Response(data, status=404)

    elif index < 10:
        data = {
            "next": None,
            "has_more": False,
            "posts": serializer.data
        }
        return Response(data)

    data = {
        "next": posts[index-1].id,
        "has_more": True,
        "posts": serializer.data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_post(request, username, last_post):
    channel = list(Channel.objects.filter(members__username=username).filter(members__pk=request.user.pk).values_list('id'))
    posts = Post.objects.filter(posted_in__in=channel, is_hidden=False, id__lt=last_post).order_by('-pk').distinct()
    serializer = PostSerializer(posts, many=True)

    index = posts.count()

    if index < 0:
        data = {
            "msg": "No posts found.",
        }
        return Response(data, status=404)

    elif index < 10:
        data = {
            "next": None,
            "has_more": False,
            "posts": serializer.data
        }
        return Response(data)

    data = {
        "next": posts[index - 1].id,
        "has_more": True,
        "posts": serializer.data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_post(request, channel_name, last_post):
    channel = Channel.objects.get(name=channel_name)
    member_of = UserProfile.objects.get(id=request.user.pk).channel_set.all()

    if channel not in member_of:
        return Response({'msg': 'Not a member of channel'}, status=401)

    if not channel.is_active:
        return Response({'msg': 'Channel not active'}, status=403)

    posts = Post.objects.filter(posted_in=channel.pk, is_hidden=False, id__lt=last_post).order_by('-pk').distinct()[:10]
    serializer = PostSerializer(posts, many=True)

    index = posts.count()

    if index < 0:
        data = {
            "msg": "No posts found.",
        }
        return Response(data, status=404)

    elif index < 10:
        data = {
            "next": None,
            "has_more": False,
            "posts": serializer.data
        }
        return Response(data)

    data = {
        "next": posts[index - 1].id,
        "has_more": True,
        "posts": serializer.data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id, last_comment):
    comments = PostComments.objects.filter(post=post_id, id__lt=last_comment).order_by('-pk')[:4]

    serializer = CommentSerializer(comments, many=True)

    index = comments.count()

    if index < 0:
        data = {
            "msg": "No posts found.",
        }
        return Response(data, status=404)

    elif index < 4:
        data = {
            "next": None,
            "has_more": False,
            "comment": serializer.data
        }
        return Response(data)

    data = {
        "next": comments[index - 1].id,
        "has_more": True,
        "comment": serializer.data
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post_like(request, post_id):
    try:
        like = PostLikes.objects.get(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.delete()
    except PostLikes.DoesNotExist:
        like = PostLikes(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.save()

    return Response({'msg': 'updated post like'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    data = json.loads(request.POST['data'])

    # check if channel list is empty

    if data['channel_list'] == []:
        return Response(status=400)

    # check if user is member of all channels

    user_channel = list(UserProfile.objects.get(pk=request.user.pk).channel_set.all().values_list('id'))
    channel_member_list = list(map(lambda x: x[0], user_channel))

    post_channel_list = list(map(lambda x: x['id'], data['channel_list']))

    """
        all( channel in channel_member_list for channel in post_channel_list )
        above function does somthing similar
        https://stackoverflow.com/questions/16579085/how-can-i-verify-if-one-list-is-a-subset-of-another
    """

    if not set(post_channel_list).issubset(set(channel_member_list)):
        return Response(status=400)

    postForm = PostForm(data)

    if postForm.is_valid():

        # Creating post

        post = Post.objects.create(body=data['body'])
        post.save()

        # post_saved signal creates user_post_media instance

        post_saved.send(sender="create post", user=request.user.pk, post=post.pk, media=None)

        # Adding Channels to the post

        for channel in data['channel_list']:
            try:
                channel = Channel.objects.get(id=channel['id'])
                post.posted_in.add(channel)
            except Channel.DoesNotExist:
                return Response(status=400)

        # Storing Files in storage and path in db

        count = 0

        for file in request.FILES:
            file = request.FILES[file]
            file_extension = file.name.split('.')[-1]
            file.name = "media_%s.%s" % (count, file_extension)

            try:
                default_storage.save("media/postFiles/post_%s/%s" % (str(post.pk), file.name), file)

                media = Media.objects.create(
                    file="postFiles/post_%s/%s" % (str(post.pk), file.name),
                    file_type=str(file.content_type)
                )
                media.save()

                count += 1

                # media_saved signal creates user_post_media instance

                media_saved.send(sender="create post", user=request.user.pk, post=post.pk, media=media.pk)

            except Exception as e:
                post.delete()
                print("exception ", e)
                return Response({"msg":"Some error occred."}, status=500)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    else:
        return Response(status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_post(request):
    data = json.loads(request.body)

    "check if channel list is empty"

    if data['channel_list'] == []:
        return Response(status=400)

    "check if user is member of all channels"

    user_channel = list(UserProfile.objects.get(pk=request.user.pk).channel_set.all().values_list('id'))
    channel_member_list = set(map(lambda x: x[0], user_channel))

    post_channel_list = set(map(lambda x: x['id'], data['channel_list']))

    """ 
        all( channel in channel_member_list for channel in post_channel_list )
        above function does somthing similar
        https://stackoverflow.com/questions/16579085/how-can-i-verify-if-one-list-is-a-subset-of-another
    """

    if not post_channel_list.issubset(channel_member_list):
        return Response(status=400)

    postForm = PostForm(data)

    if postForm.is_valid():
        post = Post.objects.get(pk=data['post_id'])
        post.body = "Edited : \n\n" + data['body']
        post.save()

        old_post_channel_list = set(map(lambda x: x[0], post.posted_in.all().values_list('id')))

        added_channels = post_channel_list.difference(old_post_channel_list)
        removed_channels = old_post_channel_list.difference(post_channel_list)

        for channel_id in added_channels:
            post.posted_in.add(Channel.objects.get(id=channel_id))

        for channel_id in removed_channels:
            post.posted_in.remove(Channel.objects.get(id=channel_id))

        post_media = UserPostMedia.objects.filter(post_id=1, media_id__isnull=False)
        for media in post_media:
            media.delete()
        default_storage.save("postFiles/post_%s" % (str(post.pk)))

        count = 0
        for file in request.FILES:
            file = request.FILES[file]
            file_extension = file.name.split('.')[-1]
            file.name = "media_%s.%s" % (count, file_extension)

            try:
                default_storage.save("postFiles/post_%s/%s" % (str(post.pk), file.name), file)

                media = Media.objects.create(
                    file=fileURL,
                    file_type=str(file.content_type)
                )
                media.save()

                count += 1

                # media_saved signal creates user_post_media instance

                media_saved.send(sender="create post", user=request.user.pk, post=post.pk, media=media.pk)

            except Exception as e:
                post.delete()
                print("exception ", e)
                return Response({"msg":"Some error occred."}, status=500)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    else:
        return Response(status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_comment(request):
    data = json.loads(request.body)

    try:
        post = Post.objects.get(id=data['post'])
        commentForm = CommentForm(data)

        if commentForm.is_valid():
            comment = PostComments.objects.create(
                user_id=request.user.pk,
                post_id=data['post'],
                body=data['body']
            )
            comment.save()
        else:
            return Response(status=400)
    except Post.DoesNotExist:
        return Response(status=400)

    comments = PostComments.objects.get(id=comment.pk)
    serializer = CommentSerializer(comments)

    return Response(serializer.data)
