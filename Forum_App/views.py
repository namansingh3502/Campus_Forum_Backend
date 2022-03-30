from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.files.storage import default_storage
import json

from .signals import media_saved
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
def posts_user(request):

    channel = list(UserProfile.objects.get(pk=request.user.pk).channel_set.all().values_list('id'))
    post_id = Post.objects.filter(posted_in__in=channel, is_hidden=False).order_by('-pk').distinct()
    serializer = PostSerializer(post_id, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id):

    comments = Post_Comment.objects.filter(post=post_id).order_by('pk')
    serializer = CommentSerializer(comments, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_likes(request, post_id):

    likes = Post_Like.objects.filter(post=post_id)
    serializer = LikeSerializer(likes, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_details(request, channel_id):

    try:
        data = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({'msg':'Channel does not exist'}, status=404)

    serializer = ChannelDetailsSerializer(data)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channel_post(request, channel_id):

    channel = Channel.objects.get(id=channel_id)
    member_of = UserProfile.objects.get(id=request.user.pk).channel_set.all()

    if channel not in member_of:
        return Response({'msg':'Not a member of channel'}, status=401)

    if not channel.is_active:
        return Response({'msg':'Channel not active'}, status=403)

    post_id = Post.objects.filter(posted_in=channel_id, is_hidden=False).order_by('-pk').distinct()
    serializer = PostSerializer(post_id, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post_like(request, post_id):

    try:
        like = Post_Like.objects.get(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.delete()
    except Post_Like.DoesNotExist:
        like = Post_Like(
            user_id=request.user.pk,
            post_id=post_id
        )
        like.save()

    return Response({'msg':'updated post like'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post(request):
    data = json.loads(request.POST['data'])

    # check if channel list is empty

    if data['channel_list'] == []:
        return Response(status=400)

    #check if user is member of all channels

    user_channel = list(UserProfile.objects.get(pk=request.user.pk).channel_set.all().values_list('id'))
    channel_member_list = list(map(lambda x: x[0], user_channel))

    post_channel_list = list(map(lambda x : x['id'], data['channel_list']))

    """
        all( channel in channel_member_list for channel in post_channel_list )
        above function does somthing similar
        https://stackoverflow.com/questions/16579085/how-can-i-verify-if-one-list-is-a-subset-of-another
    """

    if not set(post_channel_list).issubset(set(channel_member_list)) :
        return Response(status=400)

    postForm = PostForm(data)

    if postForm.is_valid():

        #Creating post

        post = Post.objects.create(
            body = data['body'],
            media_count = data['media_count']
        )
        post.save()

        # post_saved signal creates user_post_media instance

        # post_saved.send(sender="create post", user=request.user.pk, post=post.pk, media=None)

        #Adding Channels to the post

        for channel in data['channel_list']:
            try:
                channel = Channel.objects.get(id=channel['id'])
                post.posted_in.add(channel)
            except Channel.DoesNotExist:
                return Response(status=400)

        #Storing Files in storage and path in db

        index = 0
        for file in request.FILES:
            file = request.FILES[file]
            file_extension = file.name.split('.')[-1]
            file.name = "media_" + str(index) + '.' + file_extension


            try:
                default_storage.save("postFiles/" + file.name, file)

                firebaseStorage.child(
                        "postFiles/post_" + str(post.pk) + "/" + file.name
                    ).put(
                        "media/" + "postFiles/" + file.name
                    )

                fileURL = firebaseStorage.child(
                        "postFiles/post_" + str(post.pk) + "/" + file.name
                    ).get_url(
                        token="9bb2e73f-6b9a-42a1-bef9-78e1794c2a3f"
                    )

                media = Media.objects.create(
                    file=fileURL,
                    file_type=str(file.content_type)
                )
                media.save()

                default_storage.delete("postFiles/" + file.name)
                index += 1

                #media_saved signal creates user_post_media instance

                media_saved.send(sender="create post", user=request.user.pk, post=post.pk, media=media.pk)

            except Exception as e:
                post.delete()
                print("exception ", e)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    else:
        return Response(status=400)

    return Response({'msg':'unknown error while creating post.'})


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

    post_channel_list = set(map(lambda x : x['id'], data['channel_list']))

    """ 
        all( channel in channel_member_list for channel in post_channel_list )
        above function does somthing similar
        https://stackoverflow.com/questions/16579085/how-can-i-verify-if-one-list-is-a-subset-of-another
    """

    if not post_channel_list.issubset(channel_member_list) :
        return Response(status=400)

    postForm = PostForm(data)

    if postForm.is_valid():
        post = Post.objects.get(pk=data['post_id'])
        post.body = data['body']
        post.save()

        old_post_channel_list = set(map(lambda x: x[0], post.posted_in.all().values_list('id')))

        added_channels = post_channel_list.difference(old_post_channel_list)
        removed_channels = old_post_channel_list.difference(post_channel_list)

        for channel_id in added_channels :
            post.posted_in.add(Channel.objects.get(id=channel_id))

        for channel_id in removed_channels:
            post.posted_in.remove(Channel.objects.get(id=channel_id))

        serializer = PostSerializer(post)
        return Response(serializer.data)

    else:
        return Response(status=400)

    return Response({'msg':'iunknown error while editing post.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_comment(request):

    data = json.loads(request.body)

    try:
        post = Post.objects.get(id=data['post'])
        commentForm = CommentForm(data)

        if commentForm.is_valid():
            comment = Post_Comment.objects.create(
                user_id=request.user.pk,
                post_id=data['post'],
                body=data['body']
            )
            comment.save()
        else:
            return Response(status=400)
    except Post.DoesNotExist:
        return Response(status=400)

    comments = Post_Comment.objects.get(id=comment.pk)
    serializer = CommentSerializer(comments)

    return Response(serializer.data)