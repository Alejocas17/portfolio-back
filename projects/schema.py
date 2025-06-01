import graphene
from graphene_django.types import DjangoObjectType
from .models import Project, User

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project


# UserType definition
class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    project = graphene.Field(ProjectType, id=graphene.Int())

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_project(root, info, id):
        return Project.objects.get(pk=id)

class CreateProject(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        tech_stack = graphene.List(graphene.String, required=True)
        repo_url = graphene.String()
        live_demo_url = graphene.String()
        image_url = graphene.String()
        user_id = graphene.Int(required=True)  # foreign key

    project = graphene.Field(ProjectType)

    def mutate(self, info, title, description, tech_stack, user_id, repo_url=None, live_demo_url=None, image_url=None):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

        project = Project.objects.create(
            title=title,
            description=description,
            tech_stack=tech_stack,
            repo_url=repo_url,
            live_demo_url=live_demo_url,
            image_url=image_url,
            user=user
        )
        return CreateProject(project=project)
# CreateUser mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email):
        user = User(username=username, email=email)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)