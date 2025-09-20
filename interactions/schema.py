import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model
from .models import Like, Comment, Share
from posts.models import Post

User = get_user_model()


# GraphQL Types
class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ("id", "user", "post", "created_at")


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content", "created_at")


class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = ("id", "user", "post", "message", "created_at")


# Queries
class Query(graphene.ObjectType):
    likes = graphene.List(LikeType, post_id=graphene.Int(required=False))
    comments = graphene.List(CommentType, post_id=graphene.Int(required=True))
    shares = graphene.List(ShareType, post_id=graphene.Int(required=False))

    def resolve_likes(root, info, post_id=None):
        if post_id:
            return Like.objects.filter(post_id=post_id)
        return Like.objects.all()

    def resolve_comments(root, info, post_id):
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def resolve_shares(root, info, post_id=None):
        if post_id:
            return Share.objects.filter(post_id=post_id)
        return Share.objects.all()


# Mutations
class LikePost(graphene.Mutation):
    like = graphene.Field(LikeType)

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            raise GraphQLError("You already liked this post")

        return LikePost(like=like)


class UnlikePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        post_id = graphene.Int(required=True)

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            like = Like.objects.get(user=user, post_id=post_id)
            like.delete()
            return UnlikePost(success=True)
        except Like.DoesNotExist:
            raise GraphQLError("You haven’t liked this post")


class AddComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        comment = Comment.objects.create(user=user, post=post, content=content)
        return AddComment(comment=comment)


class DeleteComment(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        comment_id = graphene.Int(required=True)

    def mutate(self, info, comment_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            comment = Comment.objects.get(pk=comment_id, user=user)
            comment.delete()
            return DeleteComment(success=True)
        except Comment.DoesNotExist:
            raise GraphQLError("Comment not found or not authorized")


class SharePost(graphene.Mutation):
    share = graphene.Field(ShareType)

    class Arguments:
        post_id = graphene.Int(required=True)
        message = graphene.String(required=False)

    def mutate(self, info, post_id, message=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")

        share = Share.objects.create(user=user, post=post, message=message)
        return SharePost(share=share)


class Mutation(graphene.ObjectType):
    like_post = LikePost.Field()
    unlike_post = UnlikePost.Field()
    add_comment = AddComment.Field()
    delete_comment = DeleteComment.Field()
    share_post = SharePost.Field()
