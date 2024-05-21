import graphene
from graphene_django import DjangoObjectType
from mil_records.schema import Query as user_Q 
from mil_records.mutations import Mutation as user_M
from user.schema import Query as users_Q
from user.mutation import Mutation as users_M

class Query(user_Q,users_Q,graphene.ObjectType):
    home = graphene.String()

    def resolve_home(self, info):
        return f"Welcome User"

class Mutation(user_M,users_M,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)