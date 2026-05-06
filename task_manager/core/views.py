from django.utils.timezone import now
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .models import Project, Membership, User, Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import SignupSerializer, AddMemberSerializer, TaskSerializer
# Create your views here.


def root_view(request):
    return HttpResponse("Server is running 🚀")

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Project, Membership
from core.serializer import ProjectSerializer

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # show only projects where user is a member
        projects = Project.objects.filter(memberships__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            project = serializer.save(created_by=request.user)

            # 👇 VERY IMPORTANT
            Membership.objects.create(
                user=request.user,
                project=project,
                role='ADMIN'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        serializer = AddMemberSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # 🔒 Check if current user is ADMIN
        try:
            membership = Membership.objects.get(
                user=request.user,
                project_id=project_id
            )
        except Membership.DoesNotExist:
            return Response({"error": "Not a project member"}, status=403)

        if membership.role != 'ADMIN':
            return Response({"error": "Only admin can add members"}, status=403)

        # ✅ Add new member
        user = User.objects.get(id=serializer.validated_data['user_id'])

        Membership.objects.create(
            user=user,
            project_id=project_id,
            role=serializer.validated_data['role']
        )

        return Response({"message": "Member added"}, status=201)

class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # show tasks only from projects user belongs to
        tasks = Task.objects.filter(project__memberships__user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            project = serializer.validated_data['project']

            # 🔒 ensure user belongs to project
            if not Membership.objects.filter(user=request.user, project=project).exists():
                return Response({"error": "Not part of this project"}, status=403)

            task = serializer.save()
            return Response(TaskSerializer(task).data, status=201)

        return Response(serializer.errors, status=400)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(project__memberships__user=request.user)

        total = tasks.count()
        completed = tasks.filter(status='DONE').count()
        pending = tasks.exclude(status='DONE').count()
        overdue = tasks.filter(due_date__lt=now(), status__in=['TODO', 'IN_PROGRESS']).count()

        return Response({
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "overdue_tasks": overdue
        })

