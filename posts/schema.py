import graphene
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "author", "content", "image", "created_at")


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    feed = graphene.List(PostType)

    def resolve_posts(root, info):
        return Post.objects.all().order_by("-created_at")

    def resolve_post(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

    def resolve_feed(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        followed_ids = user.following.values_list("following_id", flat=True)
        return Post.objects.filter(author_id__in=followed_ids).order_by("-created_at")


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)
        image = Upload(required=False)

    def mutate(self, info, content, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        post = Post.objects.create(author=user, content=content, image=image)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        id = graphene.Int(required=True)
        content = graphene.String(required=False)
        image = Upload(required=False)

    def mutate(self, info, id, content=None, image=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            post = Post.objects.get(pk=id, author=user)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not authorized")

        if content:
            post.content = content
        if image:
            post.image = image
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            post = Post.objects.get(pk=id, author=user)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not authorized")


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

