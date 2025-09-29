from rest_framework_mongoengine import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status

from mongoengine import Q

from courses.models import Courses

from .models import Surveys, Answers, Questions
from .serializers import SurveySerializer, QuestionSerializer, AnswersSerializer
from api.validators import StudentPermission, TeacherPermission, AdminPermission

class SurveysViewSet(viewsets.ModelViewSet):
    permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
    ]
    queryset = Surveys.objects()
    serializer_class = SurveySerializer

    def list(self, request):
        global queryset
        if request.query_params:
            filter_q = Q()
            for key, value in request.query_params.items():
                related_fields = { 
                    "course_id": int
                }
                if hasattr(Surveys, key):
                    if key in related_fields.keys():
                        try:
                            value = int(value)
                        except:
                            pass
                        if type(value) == related_fields[key]:
                            filter_q &= Q(**{key: value})
                        else:
                            return Response({ "error": f"El filtro {value} no coincide con el valor {related_fields[key]}" },status=400)
                    else:
                        filter_q &= Q(**{key: value})
                else:
                    return Response({ "error": "Columna no encontrada a filtrar" }, status=400)
                
            queryset = list(Surveys.objects().filter(filter_q))
            if len(queryset) == 0:
                return Response(queryset)
        else:
            queryset = list(Surveys.objects())
    
        surveys = []

        for survey in queryset:
            survey_obj = {
                "id": str(survey.id),
                "title": survey.title,
                "description": survey.description,
                "course": {},
                "created_at": survey.created_at,
                "questions": [],
            }
            try:
                course_obj = Courses.objects.get(id=survey.course_id)
                survey_obj["course"] = {
                    "id": course_obj.id,
                    "title": course_obj.title,
                    "description": course_obj.description,
                    "user": {
                        "first_name": course_obj.user.first_name,
                        "last_name": course_obj.user.last_name,
                    },
                    "created_at": course_obj.created_at,
                }
            except Exception as error:
                print(error)
                return Response([], status=404)
            for question in survey.question_id:
                try:
                    question_obj = Questions.objects.get(id=str(question.id))
                    questions_obj = {
                            "id": str(question_obj.id),
                            "question": question_obj.question,
                            "answers": [],
                        }
                    for answer_id in question.answers_id: 
                        answer_obj = Answers.objects.get(id=str(answer_id.id))
                        questions_obj["answers"].append({
                            "id": str(answer_obj.id),
                            "answer": answer_obj.answer, 
                            "is_correct": answer_obj.is_correct
                        })
                    survey_obj["questions"].append(questions_obj)
                except Exception as error:
                    print(error)
                    return Response({"error":"error en la pregunta y respuesta!"})
            surveys.append(survey_obj)
        return Response(surveys)


    
    
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        survey_obj = serializer.data
        survey_obj["questions"] = []

        course_id = survey_obj.get('course_id')

        if course_id:
            try:
                course_obj = Courses.objects.get(id=course_id) 
                survey_obj['course_id'] = {
                    'id': course_obj.id,
                    'title': course_obj.title,
                    'description': course_obj.description,
                }
            except Courses.DoesNotExist:
                return Response({"error": "error en id"})

        for question_id in  survey_obj["question_id"]:
            try:
                question_obj = Questions.objects.get(id=question_id)
                question_list = {
                        "id": str(question_obj.id),
                        "question": question_obj.question,
                        "answers": []
                    }
                for answer_id in question_obj.answers_id:
                    answer_obj = Answers.objects.get(id=str(answer_id.id))
                    answers = {
                        "id": str(answer_obj.id),
                        "answer": answer_obj.answer,
                        "is_correct": answer_obj.is_correct,
                    }
                    question_list["answers"].append(answers)
                survey_obj["questions"].append(question_list)
                
            except Exception as error:
                print(error)
                return Response({"error":"error en obtener el id"})
        del survey_obj["question_id"]
        return Response(survey_obj)
    

class QuestionsViewSet(viewsets.ModelViewSet):
    permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
    ]
    queryset = Questions.objects()
    serializer_class = QuestionSerializer

    

    def create(self, request, *args, **kwargs ):
        datos = request.data
        serializador = self.serializer_class(data=datos)
        answer = datos.get('answers_id')

        if not serializador.is_valid():
            return Response(serializador.errors)
        
        if not "answers_id" in datos.keys():
             return Response({'answers_id': 'El valor de "answers_id" no se a encontrado'})

        else:
            if type(answer) != list:
                 return Response({'answers_id': 'El valor de "answers_id" no es un arreglo'})
            else:
                if len(answer) == 0:
                     return Response({'answers_id': 'la lista "answers_id" esta vacio'})
                else:
                    for answer_id in answer: 
                        try:
                            Answers.objects.get(id=answer_id)
                        except Answers.DoesNotExist:
                            return Response({'answers_id': f'No se encontró la respuesta con el ID: {answer_id}'})
        serializador.save()
        return Response(serializador.data)
    

    def list(self, request):
        queryset = Questions.objects()
        questions = []
        for question in queryset:
            question_obj =   {
                    "id": str(question.id),
                    "question": question.question,
                    "answers":[],
                }
            for answers in question.answers_id:
                try:
                    answers_obj = Answers.objects.get(id=str(answers.id))
                    question_obj ["answers"].append({ 
                        "answer": answers_obj.answer,
                        "is_correct": answers_obj.is_correct, 
                    })
                except Exception as error:
                    print(error)
                    return Response({"error":"respuesta no encontrado"})
            questions.append(question_obj)
        return Response(questions)
 
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        question_obj = serializer.data
        question_obj["answers"] = []

        for answers in question_obj["answers_id"]:
            try:
                answers_obj = Answers.objects.get(id=answers)
                question_obj["answers"].append ({ 
                    "answer": answers_obj.answer, 
                    "is_correct": answers_obj.is_correct 
                })
            except Exception as error:
                print(error)
                return Response({"error":"error con los answers"})
        del question_obj["answers_id"]
        return Response(question_obj)
        


class AnswersViewSet(viewsets.ModelViewSet):
    permission_classes = [
    StudentPermission | TeacherPermission | AdminPermission
    ]
    queryset = Answers.objects()
    serializer_class = AnswersSerializer