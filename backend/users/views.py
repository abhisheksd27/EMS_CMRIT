from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class AdminRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'ADMIN'  # Set the role to Admin
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HODRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'HOD'  # Set role to HOD
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrincipalRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'PRINCIPAL'  # Set role to Principal
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['role'] = 'STUDENT'  # Set role to Student
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
# Admin Login View
class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate using email as the username
        user = authenticate(username=email, password=password)

        if user is not None and user.role == 'ADMIN':
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials or role'}, status=status.HTTP_400_BAD_REQUEST)


# HOD Login View
class HODLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        branch = request.data.get('branch')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user is not None and user.role == 'HOD' and user.branch == branch:
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials or role'}, status=status.HTTP_400_BAD_REQUEST)

# Principal Login View
class PrincipalLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user is not None and user.role == 'PRINCIPAL':
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials or role'}, status=status.HTTP_400_BAD_REQUEST)

# Student Login View
# class StudentLoginView(APIView):
#     def post(self, request):
#         email_or_usn = request.data.get('email_or_usn')
#         password = request.data.get('password')
        
#         # Login using either email or USN
#         try:
#             user = User.objects.get(email=email_or_usn)
#         except User.DoesNotExist:
#             try:
#                 user = User.objects.get(usn=email_or_usn)
#             except User.DoesNotExist:
#                 user = None

#         if user is not None and user.check_password(password) and user.role == 'STUDENT':
#             tokens = get_tokens_for_user(user)
#             return Response(tokens, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials or role'}, status=status.HTTP_400_BAD_REQUEST)







class StudentLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Attempting to log in user with email: {email}")  # Debug line

        try:
            user = User.objects.get(email=email)
            print(f"User found: {user}")  # Debug line
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            print(f"Password matches for user: {user}")  # Debug line
            if user.role == 'STUDENT':
                tokens = get_tokens_for_user(user)  # Generate tokens
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
