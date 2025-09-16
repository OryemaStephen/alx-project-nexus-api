import graphene
import graphql_jwt

# Import app-level schemas
import users.schema
import posts.schema
import interactions.schema


class Query(
    users.schema.Query,
    posts.schema.Query,
    interactions.schema.Query,
    graphene.ObjectType,
):
    # Combines queries from all apps
    pass


class Mutation(
    users.schema.Mutation,
    posts.schema.Mutation,
    interactions.schema.Mutation,
    graphene.ObjectType,
):
    # Add JWT auth mutations globally
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
