from typing import Counter
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from django.contrib.auth import get_user_model
import io
from .utility import clean_sen, clean_sen_spa
from .sustain import model_spanish, model, tokenizer, tokenizer_spanish
from .models import text_table

# https://github.com/django-notifications/django-notifications

# Create your views here.

# data format - {"content": "Hello there, how are you today?", "lang": "en", "actual_value": "allowed"} or "toxic"
# data format - {"content": "Realmente eres una persona talentosa, pero no seas tan condescendiente.", "lang": "spa", "actual_value": "allowed"}
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def content_api(request):
    res = {'msg': "empty"}
    if request.method == 'POST':
        json_data = request.body
        stream  = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        res['msg'] = content_type(python_data['content'], python_data['lang'])
        
        snippet = text_table(text=python_data['content'], label=python_data['actual_value'], lang=python_data['lang'], 
                            user=request.user, predicted=res['msg'])
        snippet.save()

    else:
        raise MethodNotAllowed('%s is an invalid method type ' % (request.method))

    return Response(res, content_type='application/json')        


def content_type(input_str, lang):
    #loading the vectorizer + model
    res = ""
    if lang == 'en':
        sen = clean_sen(input_str)
        sen_trans = tokenizer.transform([sen]) # It's actually vectorizer
        p = model.predict(sen_trans)[0]
        validity = ["allowed","toxic"]
        res = res + validity[p]
    else:
        sen = clean_sen_spa(input_str)
        sen_trans = tokenizer_spanish.transform([sen])
        p = model_spanish.predict(sen_trans)[0]
        validity = ["allowed","toxic"]   
        res = res + validity[p]

    return res


# data format - {"username": None, "password": None, "is_superuser": None, "is_staff": None, "is_active": None}
@api_view(['POST'])
# Disabling the authentication
@authentication_classes([])
@permission_classes([])
def create_user_api(request):
    res = {"msg": None}
    if request.method == 'POST':
        json_data = request.body
        stream  = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        db = get_user_model()
        if python_data["is_superuser"] == True:
            user = db.objects.create_superuser(username=python_data["username"], password=python_data["password"])
        else:
            user = db.objects.create_user(username=python_data["username"], password=python_data["password"])

        res['msg'] = "creatd a new user"

    else:
        raise MethodNotAllowed('%s is an invalid method type ' % (request.method))

    return Response(res, content_type='application/json')        