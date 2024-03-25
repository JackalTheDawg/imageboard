from ..serializers import *
from django.conf import settings
import magic, requests
from io import BytesIO


class UtilityHandler:

    def define_mime(self, file, query=None):
        mime_type = magic.Magic(mime=True).from_buffer(file.read())
        result = {
            'file_extension': mime_type.split("/")[1],
            'mime': mime_type.split("/")[0]
        }

        try:
            return result[query]
        except KeyError:
            return result

    def save_content(self, file, location, extension):

        try:
            file.name.split('.')[1]

        except IndexError:
            file.name.split('.')[1] = file.name + "." + extension['file_extension']

        buffer = BytesIO()
        try:
            buffer.write(file.file.getvalue())
            buffer.seek(0)
        except AttributeError:
            #must be tested hard
            pass

        r = requests.post(settings.SIDE_SERVER_ADDRESS,
                          files=({'file': buffer}),
                          data={
                              'location': location,
                              'mime': extension['mime'],
                              'filename': file.name
                          })

        if r.status_code == 200:
            file_path = r.text
            return file_path
        else:
            raise ValueError('Something goes wrong')


class QueryHandler(UtilityHandler):

    def profile_data(self, profile_id):

        page_data = Profile.objects.get(pk=profile_id)

        data_serializer = ProfileDataSerializer(page_data).data
        data_serializer['profile_picture'] = settings.SIDE_SERVER_ADDRESS + data_serializer['profile_picture']

        posts = self.get_posts(f'user={profile_id}')

        return {"data": data_serializer, "posts": posts}


    def community_data(self, community_id):

        community_data = Community.objects.get(pk=community_id)

        data_serializer = CommunitySerializer(community_data).data
        data_serializer['image'] = settings.SIDE_SERVER_ADDRESS + data_serializer['image']

        posts = self.get_posts(f'community={community_id}')

        return {"data": data_serializer, "posts": posts}


    def get_posts(self, location):
        posts = Post.objects.filter(location=location)
        result = []

        for post in posts:
            post_data = {}
            commentary_list = []
            commentaries = post.commentary_set.all()

            for commentary in commentaries:
                commentary_data = CommentarySerializer(commentary).data
                commentary_data['content'] = settings.SIDE_SERVER_ADDRESS + commentary_data['content']
                commentary_list.append(commentary_data)

            post_serializer = PostSerializer(post).data
            post_serializer['content'] = settings.SIDE_SERVER_ADDRESS + post_serializer['content']

            post_data.update(post_serializer | {'commentary': commentary_list})

            result.append(post_data)

        return result


    def profile_list(self, id):
        follows = FollowsProfiles.objects.filter(follower=id)
        following_list = []
        for profile in follows:
            profile_data = ProfileDataSerializer(profile.page).data
            profile_data['profile_picture'] = settings.SIDE_SERVER_ADDRESS + profile_data['profile_picture']
            following_list.append(profile_data)

        return {'follows': following_list}



    def community_list(self, id):
        communities = Community.objects.filter()
        joined = Community.objects.filter(followers__in=[id])
        communities_list = []

        for community in communities:
            image = settings.SIDE_SERVER_ADDRESS + community.image
            communities_list.append({"name": community.name, "image": image})

        joined_list = []
        for community in joined:
            image = settings.SIDE_SERVER_ADDRESS + community.image
            joined_list.append({"name": community.name, "image": image})

        return {'communities': communities_list, 'joined': joined_list}



    def favorite_posts(self, profile_id):
        favorites = Post.objects.filter(liked_by__in=[profile_id])
        favorites_list = []

        for posts in favorites:
            post = PostSerializer(posts).data
            post['content'] = settings.SIDE_SERVER_ADDRESS + post['content']
            favorites_list.append(post)

        return {'favorites': favorites_list}


    def create_record(self, request):

        extension = {'mime': 'null'}
        path = None
        allowed_mime = ['image', 'video', 'gif']

        if request.FILES:
            extension = self.define_mime(request.FILES['file'])
            if extension['mime'] in allowed_mime:
                path = self.save_content(request.FILES['file'], request.data['location'], extension)
            else:
                raise 'Not allowed mime'

        methods = {
            'send-post': self.create_post,
            'commentary': self.create_commentary,
            'like': self.like_post,
            'follow': self.follow_user
        }
        try:
            methods[request.headers['type']](request, path, extension)
        except IndexError:
            raise 'Not allowed header'


    def create_post(self, request, path, extension):
        Post.objects.create(
            sender=Profile(pk=request.user.id),
            location=request.data['location'],
            mime=extension['mime'],
            content=path,
            text=request.data['text']
        )

    def create_commentary(self, request, path):
        Commentary.objects.create(
            sender=Profile(pk=request.user.id),
            post=Post(pk=request.data['postId']),
            text=request.data['text'],
            content=path
        )

    def like_post(self, request, path, extension):
        post = Post.objects.get(id=request.data['postId'])

        if post.liked_by.exists():
            post.liked_by.remove(request.user.id)
        else:
            post.liked_by.add(request.user.id)

    def follow_user(self, request, path, extension):
        try:
            record = FollowsProfiles.objects.get(follower=request.user.id,
                                                 page=request.data['pageId'])
            record.delete()

        except FollowsProfiles.DoesNotExist:

            page = Profile(pk=request.data['pageId'])
            follower = Profile(pk=request.user.id)

            FollowsProfiles.objects.create(
                page=page,
                follower=follower
            )


    def edit_settings(self, request):

        path = None
        allowed_mime = ['image']

        if request.FILES:
            extension = self.define_mime(request.FILES['file'])
            if extension['mime'] in allowed_mime:
                path = self.save_content(request.FILES['file'], request.data['location'], extension)
            else:
                raise 'Not allowed mime'

        if 'profile-settings' in request.headers['type']:
            profile = Profile.objects.get(pk=request.user.id)

            for key in request.data:
                if request.data[key] != None:
                    setattr(profile, key, request.data[key])

            if path is not None:
                profile.profile_picture = path

            profile.save()

        elif 'community-settings' in request.headers['type']:
            community = Community.objects.get(pk=request.data['communityId'])

            for key in request.data:
                if request.data[key] != None:
                    setattr(community, key, request.data[key])

            if path is not None:
                community.image = path

            community.save()

