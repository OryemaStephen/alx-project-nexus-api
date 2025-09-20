import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostType(DjangoObjectType):
    like_count = graphene.Int()
    comment_count = graphene.Int()
    share_count = graphene.Int()

    class Meta:
        model = Post
        fields = ("id", "author", "content", "image_url", "created_at")

    def resolve_like_count(self, info):
        return self.likes.count()

    def resolve_comment_count(self, info):
        return self.comments.count()

    def resolve_share_count(self, info):
        return self.shares.count()


# Queries
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

        # IDs of users this person follows
        followed_ids = user.following.values_list("following_id", flat=True)

        return Post.objects.filter(author_id__in=followed_ids).order_by("-created_at")


# Mutations
class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        content = graphene.String(required=True)
        image_url = graphene.String(required=False)

    def mutate(self, info, content, image_url=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a post")
        post = Post.objects.create(author=user, content=content, image_url=image_url)
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        id = graphene.Int(required=True)
        content = graphene.String(required=False)
        image_url = graphene.String(required=False)

    def mutate(self, info, id, content=None, image_url=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")
        try:
            post = Post.objects.get(pk=id, author=user)  # ownership check
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not authorized")

        if content:
            post.content = content
        if image_url:
            post.image_url = image_url
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
            post = Post.objects.get(pk=id, author=user)  # ownership check
        except Post.DoesNotExist:
            raise GraphQLError("Post not found or not authorized")
        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
