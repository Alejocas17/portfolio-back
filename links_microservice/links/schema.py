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

class LinkOrderInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    order = graphene.Int(required=True)

class ReorderLinks(graphene.Mutation):
    class Arguments:
        orders = graphene.List(LinkOrderInput, required=True)

    ok = graphene.Boolean()
    updated_count = graphene.Int()

    def mutate(self, info, orders):
        updated = 0
        for item in orders:
            try:
                link = Link.objects.get(pk=item.id)
                link.order = item.order
                link.save()
                updated += 1
            except Link.DoesNotExist:
                continue

        return ReorderLinks(ok=True, updated_count=updated)

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

class UpdateLink(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        url = graphene.String()
        icon = graphene.String()
        category = graphene.String()
        order = graphene.Int()
        is_active = graphene.Boolean()

    link = graphene.Field(LinkType)

    def mutate(self, info, id, title=None, url=None, icon=None, category=None, order=None, is_active=None):
        try:
            link = Link.objects.get(pk=id)
        except Link.DoesNotExist:
            raise Exception("Link not found")

        if title is not None:
            link.title = title
        if url is not None:
            link.url = url
        if icon is not None:
            link.icon = icon
        if category is not None:
            link.category = category
        if order is not None:
            link.order = order
        if is_active is not None:
            link.is_active = is_active

        link.save()
        return UpdateLink(link=link)

class DeleteLink(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            link = Link.objects.get(pk=id)
            link.delete()
            return DeleteLink(ok=True, message="Link deleted successfully.")
        except Link.DoesNotExist:
            return DeleteLink(ok=False, message="Link not found.")
class DeleteLink(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            link = Link.objects.get(pk=id)
            link.delete()
            return DeleteLink(ok=True, message="Link deleted successfully.")
        except Link.DoesNotExist:
            return DeleteLink(ok=False, message="Link not found.")
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_user = CreateUser.Field()
    update_link = UpdateLink.Field()
    delete_link = DeleteLink.Field()
    reorder_links = ReorderLinks.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)