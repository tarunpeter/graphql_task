import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene_django_extras.fields import DjangoFilterPaginateListField
from graphql_jwt.decorators import login_required
from .models import UserRecord
from django.db.models import Q

class UserRecordType(DjangoObjectType):
    class Meta:
        model = UserRecord
        fields = "__all__"
        filter_fields = {
            "id": ("exact",),
            "name": ("icontains", "iexact"),
            "email": ("icontains", "iexact"),
        }

class Query(graphene.ObjectType):
    list_user_records = DjangoFilterPaginateListField(UserRecordType,search=graphene.String(),pagination = LimitOffsetGraphqlPagination(ordering="name"))

    @login_required
    def resolve_list_user_records(root, info, search=None, **kwargs):
        queryset = UserRecord.objects.all()
        if search:
            queryset = queryset.filter(Q(name__icontains=search)|Q(email__icontains=search))
        return queryset
