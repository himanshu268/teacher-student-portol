from rest_framework.views import APIView
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from django.shortcuts import render,HttpResponse,redirect
from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth.hashers import make_password,check_password
import jwt,datetime


class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return render(request,'signin.html')
    def get(self,request):
        return render(request,'signup.html')
class LoginView(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        # print(password)
        user=User.objects.filter(username=username).first()
        # print(user.password)
        # print(check_password(password,user.password))
        if user is None:
            raise AuthenticationFailed('user not found')

        if password!=user.password:
            raise AuthenticationFailed('password is incorrect')
        
        
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token=jwt.encode(payload,'secret',algorithm='HS256')
        print(token)
        if user.category=='teacher':
            response =render(request,'home.html',{'name':user.username})
        else:
            response =render(request,'student.html',{'name':user.username})


        response.set_cookie(key='jwt',value=token,httponly=True)
        # print(response)
        # if user.category=='student':
            # return response and render(request,'student.html',{'name':user.username})
        return response 
    def get(self,request):
        token = request.COOKIES.get('jwt')
        # print(token)

        if not token:
            # raise AuthenticationFailed('Unautheticated!')
            return render(request,'signin.html')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        
        user=User.objects.filter(id=payload['id']).first()
        if user.category=='student':
            return render(request,'student.html',{'name':user.username})
        return render(request,'home.html',{'name':user.username})
        

    
class UploadFeed(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        # print(token)

        if not token:
            raise AuthenticationFailed('Unautheticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        
        user=User.objects.filter(id=payload['id']).first()
        if user.category=='student':
            return HttpResponse('fuck you')
        return render(request,'upload.html')
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unautheticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        
        user=User.objects.filter(id=payload['id']).first()
        caption=request.POST.get('caption')
        teacher=user.username
        student=request.POST.get('student')
        data=Document(caption=caption,teacher=teacher,student=student)
        data.save()
        return render(request,'home.html')
        
        
class ShowFeed(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unautheticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        user=User.objects.filter(id=payload['id']).first()
        data=Document.objects.all()
        teacher=[]
        student=[]
        caption=[]
        ids=[]
        y=0
        if user.category=='teacher':
            for i in data:
                if i.teacher==user.username:
                    ids.append(i.ids)
                    student.append(i.student)
                    caption.append(i.caption)

                    y+=1
            if y==0:
                return HttpResponse('no feed available')
        
            mylist=zip(ids,student,caption)
            cont={'mylist':mylist,}
            return render(request,'teacher_feed.html',cont)
        else:
            for i in data:
                if i.student==user.username:
                    teacher.append(i.teacher)
                    caption.append(i.caption)

                    y+=1
            if y==0:
                return HttpResponse('no feed available')
        
            mylist=zip(teacher,caption)
            cont={'mylist':mylist,}
            return render(request,'student_newsfeed.html',cont)

    def delete(request,id):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unautheticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        user=User.objects.filter(id=payload['id']).first()
        dele=Document.objects.get(ids=id,teacher=user.username)
        dele.delete()
        data=Document.objects.all()
        student=[]
        caption=[]
        ids=[]
        y=0
        for i in data:
            if i.teacher==user.username:
                ids.append(i.ids)
                student.append(i.student)
                caption.append(i.caption)
                y+=1
        if y==0:
            return HttpResponse('no feed available')
        
        mylist=zip(ids,student,caption)
        cont={'mylist':mylist,}
        return render(request,'teacher_feed.html',cont)
    
    def put(request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unautheticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return render(request,'signin.html')
        user=User.objects.filter(id=payload['id']).first()
        ids=request.POST.get('ids')
        caption=request.POST.get('caption')
        if Document.objects.filter(ids=ids,teacher=user.username).exists():
            accept=Document.objects.get(ids=ids,teacher=user.username)
            accept.caption=caption
            accept.save()
        data=Document.objects.all()
        student=[]
        caption=[]
        ids=[]
        y=0
        for i in data:
            if i.teacher==user.username:
                ids.append(i.ids)
                student.append(i.student)
                caption.append(i.caption)
                y+=1
        if y==0:
            return HttpResponse('no feed available')
        
        mylist=zip(ids,student,caption)
        cont={'mylist':mylist,}
        return render(request,'teacher_feed.html',cont)
class LogoutView(APIView):
    def post(self, request):
        response=render(request,'signin.html')
        response.delete_cookie('jwt')
        # response.data={"message":"logout sucessfully"}
        return response
    def get(self, request):
        return render(request,'signin.html')


    
