import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.contrib.auth import get_user_model, authenticate
import graphql_jwt
from .models import Follow
from .tasks import send_login_notification  # Celery task

UserModel = get_user_model()


# ---------------------- GraphQL Types ----------------------
class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = ("id", "username", "email", "bio", "profile_picture")


class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")


# ---------------------- Queries ----------------------
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    followers = graphene.List(UserType, user_id=graphene.Int(required=True))
    following = graphene.List(UserType, user_id=graphene.Int(required=True))

    def resolve_users(root, info):
        return UserModel.objects.all()

    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to view this information")
        return user

    def resolve_followers(root, info, user_id):
        return [f.follower for f in Follow.objects.filter(following_id=user_id)]

    def resolve_following(root, info, user_id):
        return [f.following for f in Follow.objects.filter(follower_id=user_id)]


# ---------------------- Mutations ----------------------
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = UserModel(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class FollowUser(graphene.Mutation):
    follow = graphene.Field(FollowType)

    class Arguments:
        user_id = graphene.Int(required=True)

    def mutate(self, info, user_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")
        if user.id == user_id:
            raise GraphQLError("You cannot follow yourself")

        target = UserModel.objects.get(pk=user_id)
        follow, created = Follow.objects.get_or_create(follower=user, following=target)
        if not created:
            raise GraphQLError("Already following this user")
        return FollowUser(follow=follow)


class UnfollowUser(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        user_id = graphene.Int(required=True)

    def mutate(self, info, user_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in")
        try:
            follow = Follow.objects.get(follower=user, following_id=user_id)
            follow.delete()
            return UnfollowUser(success=True)
        except Follow.DoesNotExist:
            raise GraphQLError("Not following this user")


# ---------------------- Custom Login Mutation (Async Notification) ----------------------
class CustomLogin(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
    message = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            raise GraphQLError("Invalid credentials")

        # Generate JWT tokens
        token = graphql_jwt.shortcuts.get_token(user)
        refresh = graphql_jwt.shortcuts.create_refresh_token(user)

        # Trigger async task (Celery) for login notification
        if user.email:
            send_login_notification.delay(
                username=user.username,
                email=user.email,
            )

        return CustomLogin(
            user=user,
            token=token,
            refresh_token=refresh,
            message=f"Welcome back, {user.username}!"
        )


# ---------------------- Root Mutation ----------------------
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()
    login = CustomLogin.Field()  # Use the async login mutation
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
