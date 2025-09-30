from rest_framework_mongoengine import viewsets
from rest_framework.response import Response

from .models import Recipes, Ingredients
from .serializers import RecipeSerializer, IngredientSerializer

from django.http import HttpResponse

from api.validators import StudentPermission, TeacherPermission, AdminPermission

from jinja2 import Environment, FileSystemLoader

import os

import pdfkit


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
    ]
    queryset = Ingredients.objects()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
    ]
    queryset = Recipes.objects.all()  
    serializer_class = RecipeSerializer

    def list(self, request):
        recipes = []
        queryset = Recipes.objects.all()  
        for recipe in queryset:
            recipe_obj =   {
                    "id": str(recipe.id),
                    "name": recipe.name,
                    "description": recipe.description,
                    "created_at": recipe.created_at,
                    "ingredient":[],
                    "steps": recipe.steps,
                }
            for ingredient in recipe.ingredient:
                try:
                    ingredient_obj = Ingredients.objects.get(id=str(ingredient.id))
                    recipe_obj ["ingredient"].append({ 
                        "id": str(ingredient_obj.id), 
                        "name": ingredient_obj.name 
                    })
                except Exception as error:
                    print(error)
                    return Response({"error":"ingrediente no encontrado"})
            recipes.append(recipe_obj)
        return Response(recipes)
    
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        recipe_obj = serializer.data
        recipe_obj["ingredients"] = []

        for ingredient_obj in recipe_obj["ingredient"]:
            try:
                ingredient = Ingredients.objects.get(id=ingredient_obj)
                recipe_obj["ingredients"].append ({ 
                    "id": str(ingredient.id), 
                    "name": ingredient.name 
                })
            except Exception as error:
                print(error)
                return Response({"error":"error con los ingredient"})
        del recipe_obj["ingredient"]
        return Response(recipe_obj)
    
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        ingredients = []
        
        if request.data.get("name"): 
            recipe.name = request.data.get("name")
        
        if request.data.get("description"): 
            recipe.description = request.data.get("description")
        
        if request.data.get("ingredient"): 
            recipe.ingredient = request.data.get("ingredient")
            
            for ingredient_id in recipe.ingredient:
                ingredient_obj = Ingredients.objects.get(id=ingredient_id)
                ingredients.append(ingredient_obj)
                
        recipe.ingredient = ingredients
        
        if request.data.get("steps"): 
            recipe.steps = request.data.get("steps")
            
        recipe.save()

        return Response({
            "name": recipe.name,
            "description": recipe.description,
            "ingredient": [str(ingredient.id) for ingredient in recipe.ingredient],
            "steps": recipe.steps
        })
        
class RecipePDFViewSet(viewsets.ModelViewSet):
  permission_classes = [
    # StudentPermission
  ]
  
  def list(self, request, recipe_id):
    global recipe
    ingredients = []
    
    try:
      recipe = Recipes.objects.get(id=recipe_id)
      for ingredient in recipe.ingredient:
        ingredients.append({
          "name": ingredient.name
        })
    except:
      return Response({ "error": "Receta no encontrada" }, status=404)

    current_dir = os.path.dirname(__file__)
    template_dir = os.path.join(current_dir,"template")

    config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf/bin/wkhtmltopdf.exe")

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("recipe_pdf.html")

    html = template.render({
      "recipe_name": recipe.name,
      "recipe_description": recipe.description,
      "recipe_ingredients": ingredients,
      "recipe_steps": recipe.steps,
    })
    
    options = {
      'orientation': 'Landscape',
      'page-size': 'A4',
      'encoding': 'UTF-8',
      'margin-top': '0mm',
      'margin-right': '0mm',
      'margin-bottom': '0mm',
      'margin-left': '0mm',
    }

    pdf = pdfkit.from_string(
      html,
      output_path=False,
      options=options,
      configuration=config
    )
    
    response = HttpResponse(content_type='application/pdf')
    response.write(pdf)

    return response