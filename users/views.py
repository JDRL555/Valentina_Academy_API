from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action

from django.contrib.auth.models import User
from django.contrib.auth import logout

from .serializers import UserSerializer

from api.validators import AdminPermission, TeacherPermission, StudentPermission

from rolepermissions.roles import get_user_roles, assign_role, remove_role

from rest_framework.decorators import permission_classes

VALID_ROLES = ["student", "teacher", "admin"]

class UsersViewSet(ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [
    TeacherPermission | AdminPermission
  ]
  
  def list(self, request):
    users = User.objects.all()
    users_list = []
    
    if len(users) == 0:
      return Response([])
    
    for user in users:
      user_role = get_user_roles(user)
      
      user_obj = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": "Rol indefinido" if len(user_role) == 0 else user_role[0].get_name(),
      }
      
      users_list.append(user_obj)
      
    return Response(users_list)
  
  def create(self, request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
      if not request.data.get("role"):
        return Response({ "role": "The role's required" }, status=400)

      if request.data["role"] not in VALID_ROLES:
        return Response({ "role": "Invalid role" }, status=400)
      
      serializer.save()
      
      user = User.objects.get(username=serializer.data['username'])
      user.set_password(serializer.data['password'])
      
      assign_role(user, request.data["role"])
      user.save()
      
      return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=400)
  
  def partial_update(self, request, pk):
    user = self.get_object()
    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    
    if serializer.is_valid():
      if request.data.get("role"):
        
        if request.data["role"] not in VALID_ROLES:
          return Response({ "role": "Invalid role" }, status=400)
        
        role = get_user_roles(user)
        
        if role[0].get_name() == request.data["role"]:
          return Response({ "error": f"User already have the role {request.data['role']}" }, status=400)
        
        remove_role(user, role[0].get_name())
        assign_role(user, request.data["role"])
        
      serializer.save()
      
      if request.data.get("password"):  
        user.set_password(request.data.get("password"))
      
      user.save()
      
      return Response({"user": serializer.data})
    return Response(serializer.errors, status=400)
  
  def destroy(self, request, pk):
    user = self.get_object()
    
    role = get_user_roles(user)
    
    remove_role(user, role[0].get_name())
    
    user.delete()
    
    return Response(status=204)

class LoginViewSet(ModelViewSet):
  permission_classes = []
  def create(self, request):
    global user
    
    try:
      user = User.objects.get(username=request.data['username'])
    except:
      return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(request.data['password']):
      return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
  
class RegisterViewSet(ModelViewSet):
  permission_classes = [] 
  def create(self, request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
      serializer.save()
      
      user = User.objects.get(username=serializer.data['username'])
      user.set_password(serializer.data['password'])
      assign_role(user, 'student')
      user.save()
      
      return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class Auth_userViewSet(ModelViewSet):
  permission_classes = []
  def list(self, request, token):
    try:
      token_object = Token.objects.get(key=token)
      user = token_object.user
      del user.password
      return Response({ 
        "user": { 
          "id": user.id,
          "first_name": user.first_name, 
          "last_name": user.last_name, 
          "username": user.username, 
          "email": user.email 
        } 
      })
    except Exception as err:
      print(err)
      return Response({ "error": "El token es invalido" }, status=status.HTTP_403_FORBIDDEN)
    
class LogoutViewSet(ModelViewSet):
  permission_classes = []
  def create(self, request, token):
      
      if not request.user.is_authenticated:
          return Response({'error': 'Usuario no logeado'}, status=status.HTTP_401_UNAUTHORIZED)

      logout(request)

      try:
          token = Token.objects.get(user=request.user)
          token.delete()
      except Token.DoesNotExist:
          pass

      return Response({'message': 'Se a cerrado la session'}, status=status.HTTP_200_OK)
    
class RolViewSet(ViewSet):
  permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
  ]
  
  def valid_role(self, rol):
    return rol in VALID_ROLES
  
  def validate_role_data(self, data):
    errors = {}
    
    if not data.get("role"): 
      errors["role"] = "El role es requerido"
    
    if not data.get("user_id"):
      errors["user_id"] = "El user_id es requerido"
    
    if len(errors.keys()) != 0:
      return { 
        "invalid_data": True, 
        "errors": errors, 
        "status": 400 
      }
    
    try:
      User.objects.get(id=data["user_id"])
    except:
      return { 
        "invalid_data": True, 
        "errors": { "user": "Usuario no encontrado" }, 
        "status": 404 
      }
    
    if not self.valid_role(data["role"]):
        return { 
        "invalid_data": True, 
        "errors": { "role": "Rol invalido. Seleccione: student, teacher, admin" }, 
        "status": 400
      }
        
    return {
      "invalid_data": False,
      "errors": {},
      "status": 200
    }
  
  def list(self, request, user_id):
    global user
    try:
      user = User.objects.get(id=user_id)
    except:
      return Response({ "error": "Usuario no encontrado" }, status=404)
    
    role = get_user_roles(user)
    
    if not role:
      return Response({
        "role": "El usuario no posee rol"
      })
    
    return Response({ 
      "user": { 
        "id": user.id, 
        "first_name": user.first_name, 
        "last_name": user.last_name, 
        "username": user.username, 
        "email": user.email, 
      }, 
      "role": role[0].get_name() 
    })      
    
    
  def create(self, request):
    result = self.validate_role_data(request.data)
    
    if result["invalid_data"]:
      return Response({ "error": result["errors"] }, status=result["status"])
    
    user = User.objects.get(id=request.data["user_id"])
    
    role = get_user_roles(user)
    
    if role:
      if role[0].get_name() == request.data["role"]:
        return Response(
          { 
            "error": f"El usuario ya posee el rol {role[0].get_name()}" 
          }, 
          status=400
        )
      
      if role[0].get_name():
        return Response({ "error": "El usuario ya posee un rol" }, status=400)
      
    assign_role(user=user, role=request.data["role"])

    return Response({"message": "Rol asignado satisfactoriamente!"})

      
  def update(self, request):
    result = self.validate_role_data(request.data)
    
    if result["invalid_data"]:
      return Response({ "error": result["errors"] }, status=result["status"])
    
    user = User.objects.get(id=request.data["user_id"])
    
    role = get_user_roles(user)
    
    if not role:
      return Response({
        "role": "El usuario no posee rol"
      })
    
    if role[0].get_name() == request.data["role"]:
      return Response(
        { 
          "error": f"El usuario ya posee el rol {role[0].get_name()}" 
        }, 
        status=400
      )
    
    remove_role(user=user, role=role[0].get_name())
    assign_role(user=user, role=request.data["role"])

    return Response({"message": "Rol asignado satisfactoriamente!"})
  
  def destroy(self, request):
    result = self.validate_role_data(request.data)
    
    if result["invalid_data"]:
      return Response({ "error": result["errors"] }, status=result["status"])
    
    user = User.objects.get(id=request.data["user_id"])
    
    role = get_user_roles(user)
    
    if role[0].get_name() != request.data["role"]:
      return Response(
        { 
          "error": f"El usuario no posee el rol {request.data['role']}" 
        }, 
        status=400
      )
    
    remove_role(user=user, role=request.data["role"])
    
    return Response(status=204)