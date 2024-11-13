from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta
from django.db.models import Sum, Count, Case, When, IntegerField
import json

class RegisterLandingPage(View):
    def get(self,request):
        return render(request,"new_user/registration.html")
    
    def post(self,request):
        """
        Handles POST requests to process the user registration form submission.
        Checks for email id, if it already exists, proceeds to check the approval status and handles these probable scenarios.
        Saves the user data and creates new user if email id is found to be unique.
        Args:
            request: The HTTP request object containing form data.
        
        Returns:
            HttpResponse: Redirects the user to the appropriate page after form submission.
        """
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email_id = request.POST.get("email_id")
        password = request.POST.get("password")
        username = request.POST.get("username")
        confirm_password = request.POST.get("confirm_password")
        stream = None
        if User.objects.filter(email=email_id).exists():
            User.objects.filter(email = email_id).first()
            return redirect('login')  
        hashed_password = make_password(confirm_password) 
        User(first_name= first_name,last_name=last_name,email = email_id,password = hashed_password,username=username).save()
        return redirect("login")
    
# Login Working
class LoginLandingPage(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect("home")
        
        return render(request,"new_user/new_login.html")

    def post(self,request):
        """
        Handles POST requests to process the user login form submission.
        
        Args:
            request: The HTTP request object containing form data.
        
        Returns:
            HttpResponse: Redirects the user to the appropriate page based on authentication and approval status.
        """
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Credential")
            return redirect("login")

class Logout(LoginRequiredMixin, View):
    login_url = "login"

    def get(self,request):
        logout(request)

        return redirect('login')


class Home(LoginRequiredMixin,View):
    login_url = "login"

    def get(self, request):
        return render(request,"home.html")
    
# class Result(LoginRequiredMixin,View):
#     login_url = "login"

#     def get(self, request):

#         start_test_obj = StartTest
#         available_questions = start_test_obj.get_available_questions(self,request)
        
#         if available_questions["error"]:
#             get_marks = UserResponse.objects.filter(user=request.user).aggregate(
#                 total_marks=Sum(
#                     Case(
#                         When(is_correct=True, then=1),  
#                         When(is_correct=False, then=0), 
#                         output_field=IntegerField()
#                     )
#                 ),
#                 correct_answer=Count(
#                     Case(
#                         When(is_correct=True, then=1),
#                         output_field=IntegerField()
#                     )
#                 ),
#                 incorrect_answer=Count(
#                     Case(
#                         When(is_correct=False, then=1),
#                         output_field=IntegerField()
#                     )
#                 )
#             )
#             context = {
#                 'total_marks': get_marks['total_marks'],
#                 'correct_answer': get_marks['correct_answer'],
#                 'incorrect_answer': get_marks['incorrect_answer']
#             }
#             return render(request,"pages/result_page.html",context)
#         return redirect("test_page")
    
class ResultView(LoginRequiredMixin,View):
    login_url = "login"

    def get(self, request):

        start_test_obj = StartTest
        available_questions = start_test_obj.get_available_questions(self,request)
        
        if available_questions["error"]:
            get_marks = UserResponse.objects.filter(user=request.user).aggregate(
                total_marks=Sum(
                    Case(
                        When(is_correct=True, then=1),  
                        When(is_correct=False, then=0), 
                        output_field=IntegerField()
                    )
                ),
                correct_answer=Count(
                    Case(
                        When(is_correct=True, then=1),
                        output_field=IntegerField()
                    )
                ),
                incorrect_answer=Count(
                    Case(
                        When(is_correct=False, then=1),
                        output_field=IntegerField()
                    )
                )
            )
            data = {
                'total_marks': get_marks['total_marks'],
                'correct_answer': get_marks['correct_answer'],
                'incorrect_answer': get_marks['incorrect_answer'],
                'error':False
            }
            return JsonResponse(data)
        return JsonResponse({"error":True})
   

class TestPage(View):
    login_url = "login"

    def get(self, request):
        return render(request,"pages/test_home.html")
    
    def post(self, request):
        return render(request,"pages/test_home.html")
    

class ClearResponse(LoginRequiredMixin,View):
    login_url = "login"

    def get(self, request):
        try:
            user_responses = request.user.user_response_user.all() 
            
            for user_response in user_responses:
                user_response.question.clear()
            user_responses.delete()
            data = {
                "message": "All previous responses cleared successfully.",
                "error": False,
            }
            return JsonResponse(data)

        except Exception as e:
            data = {
                "message": f"An error occurred: {str(e)}",
                "error": True,
            }
            return JsonResponse(data, status=500)
    
class StartTest(LoginRequiredMixin,View):
    login_url = "login"

    def get_available_questions(self,request):
        answered_questions  = UserResponse.objects.filter(user=request.user).values_list("question__id", flat=True).order_by("question")
        if answered_questions:
            unanswered_questions  = Questions.objects.all().exclude(id__in = answered_questions)
            if unanswered_questions:
                preview_question = unanswered_questions.first()
                data= {
                    "q_id": preview_question.id,
                    "question": preview_question.question,
                    "option_1": preview_question.option1,
                    "option_2": preview_question.option2,
                    "option_3": preview_question.option3,
                    "option_4": preview_question.option4,
                    "message":"Success",
                    "error":False
                }
                return data
            else:
                data = {
                    "message":"All Questions Answered, If you want to clear previous response . Click Okay",
                    "error":True,
                }
                return data
            
        unanswered_questions = Questions.objects.first()
        data= {
            "q_id": unanswered_questions.id,
            "question": unanswered_questions.question,
            "option_1": unanswered_questions.option1,
            "option_2": unanswered_questions.option2,
            "option_3": unanswered_questions.option3,
            "option_4": unanswered_questions.option4,
            "message":"Success",
            "error":False
        }
        return data
    
    def get(self, request):
        data = self.get_available_questions(request)
        return JsonResponse(data)

    def post(self, request):
        data = json.loads(request.body)
        q_id = data["question_id"]
        answer = str(data["answer"]).strip()
        if not q_id or not answer:
            return JsonResponse({"message": "ANswer and question id required", "error":True})
        
        get_question = Questions.objects.filter(id = q_id).first()
        if not get_question:
            return JsonResponse({"message": "Question not Found", "error":True})

        if get_question:
            marks = 1 if get_question.correct_answer == answer else 0
            user_response = UserResponse.objects.create(
                user_response=answer,
                user=request.user,
                marks=marks,
                is_correct=marks,
            )

            user_response.question.add(get_question)
        
        data = self.get_available_questions(request)
        return JsonResponse(data)
    
