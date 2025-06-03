import graphene
from graphene_django.types import DjangoObjectType
from .models import Link, User

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

# UserType definition
class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_link_by_user_id = graphene.List(LinkType, user_id=graphene.Int(required=True))
    all_link_by_user_name = graphene.List(LinkType, user_name=graphene.String(required=True))

    link = graphene.Field(LinkType, id=graphene.Int())

    get_user_by_user_name = graphene.Field(UserType, user_name=graphene.String(required=True))

    def resolve_all_link_by_user_id(root, info, user_id):
        return Link.objects.filter(user_id=user_id)
    
    def resolve_all_link_by_user_name(root, info, user_name,):
        print(user_name)
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            raise Exception("User not found")
        print(user.id)
        return Link.objects.filter(user_id=user.id, is_active=True)
    
    def resolve_link(root, info, id):
        return Link.objects.get(pk=id)
    
    def resolve_get_user_by_user_name(self, info, user_name):
        try:
            return User.objects.get(username=user_name)
        except User.DoesNotExist:
            return None


class CreateLink(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        icon = graphene.String()
        category = graphene.String()
        user_id = graphene.Int(required=True)
        order = graphene.Int(required=True)
        clicks = graphene.Int()
        is_active = graphene.Boolean()

    link = graphene.Field(LinkType)

    def mutate(self, info, title, url, order, user_id, icon=None, category=None, clicks=0, is_active=True):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

    
        link = Link.objects.create(
            title = title,
            url = url,
            icon = icon,
            category = category,
            order = order,
            clicks = clicks,
            is_active = is_active,
            user = user
        )
        return CreateLink(link=link)

# CreateUser mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        name = graphene.String(required=True)
        lastname = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, name, lastname):
        user = User(username=username, email=email, name=name, lastname=lastname)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)