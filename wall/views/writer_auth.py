from rest_framework.views import APIView
from rest_framework.response import Response

from wall.models import Writer
from wall.models import EmailValidation
from wall.models import Session

from utility import check_params
from utility import RequestResponse
from utility import send
from utility import random4
from utility import uuid36


class Registration(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['name', 'username', 'password', 'email', 'phone']):
            post_data = request.POST
            if Writer.objects.filter(email=post_data['email']).exists() or \
                    Writer.objects.filter(username=post_data['username']).exists():
                response.set_status(400)
                response.set_message('User already registered')
            else:
                user = Writer()
                user.username = post_data['username']
                user.name = post_data['name']
                user.email = post_data['email']
                user.phone = post_data['phone']
                user.password = Writer.encrypt_password(post_data['password'])
                user.save()
                four_digit_code = random4()
                new_validation = EmailValidation(writer=user,
                                                 code=four_digit_code)
                new_validation.save()
                try:
                    email_subject = 'Welcome to the Wall!'
                    link = 'http://' + request.META['HTTP_HOST'] + '/api/activate/?email=' + \
                           user.email + '&auth=' + four_digit_code
                    email_body = "Hi %s,\rwelcome to the wall. Your activation code is %s.\r\r" \
                                 "Or you can directly activate your account by clicking here: %s" \
                                 % (user.name, four_digit_code, link)
                    send(user.name, user.email, email_subject, email_body)
                except KeyError:
                    data = {'activation_code': four_digit_code}
                    response.set_data(data)
                response.set_status(200)
                response.set_message('User successfully added')

        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())


class Activate(APIView):

    @staticmethod
    def get(request):
        response = RequestResponse()
        if check_params(request.GET, ['auth', 'email']):
            get_data = request.GET
            if Writer.objects.filter(email=get_data['email']).exists():
                writer_object = Writer.objects.get(email=get_data['email'])
                if not writer_object.is_active:
                    if EmailValidation.objects.filter(code=get_data['auth'], writer=writer_object).exists():
                        validation_object = EmailValidation.objects.get(code=get_data['auth'], writer=writer_object)
                        writer_object.is_active = True
                        writer_object.save()
                        validation_object.delete()
                        response.set_status(200)
                        response.set_message('User successfully activated')
                    else:
                        response.set_status(400)
                        response.set_message('Validation code incorrect')
                else:
                    response.set_status(400)
                    response.set_message('Already activated')
            else:
                response.set_status(400)
                response.set_message('User not found')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())


class Login(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['email', 'password']):
            post_data = request.POST
            user = Writer.get_user_by_email_password(post_data['email'], post_data['password'])
            if user is not None and user.is_active:
                data = Login.create_session_for_user(user)
                response.set_data(data)
                response.set_status(200)
                response.set_message('Session created successfully')
            elif user is not None and not user.is_active:
                response.set_status(400)
                response.set_message('Account not active')
            else:
                response.set_status(400)
                response.set_message('Incorrect credentials')
        elif check_params(request.POST, ['username', 'password']):
            post_data = request.POST
            user = Writer.get_user_by_username_password(post_data['username'], post_data['password'])
            if user is not None and user.is_active:
                data = Login.create_session_for_user(user)
                response.set_data(data)
                response.set_status(200)
                response.set_message('Session created successfully')
            elif user is not None and not user.is_active:
                response.set_status(400)
                response.set_message('Account not active')
            else:
                response.set_status(400)
                response.set_message('Incorrect credentials')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())

    @staticmethod
    def create_session_for_user(user):
        session_id = uuid36()
        new_session = Session(writer=user, code=session_id)
        new_session.save()
        data = {'sid': session_id}
        return data


class Logout(APIView):

    @staticmethod
    def post(request):
        response = RequestResponse()
        if check_params(request.POST, ['sid']):
            post_data = request.POST
            if Session.objects.filter(code=post_data['sid']).exists():
                session_object = Session.objects.get(code=post_data['sid'])
                session_object.delete()
                response.set_status(200)
                response.set_message('Session removed successfully')
            else:
                response.set_status(400)
                response.set_message('Incorrect session')
        else:
            response.set_status(400)
            response.set_message('Incorrect Parameters')
        return Response(response.respond())
