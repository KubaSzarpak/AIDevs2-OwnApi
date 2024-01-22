import json

import openai
import dotenv
import os

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from serpapi import GoogleSearch

# Create your views here.


dotenv.load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY', default='')

CLIENT = openai.Client(api_key=OPENAI_API_KEY)


class Chatbot(APIView):
    def post(self, request):
        question = self.request.data.get('question', '')
        if not question:
            return HttpResponse(json.dumps({'message': 'Question is required'}), status=status.HTTP_400_BAD_REQUEST)

        response = CLIENT.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': question}
            ]
        ).choices[0].message.content

        return HttpResponse(json.dumps({'reply': response}), status=status.HTTP_200_OK, charset='utf-8')


class Google(APIView):
    def post(self, request):
        question = self.request.data.get('question', '')

        params = {
            'q': question,
            'location': 'Poland',
            'hl': 'pl',
            'gl': 'pl',
            'api_key': '53087c7bf1cae0f7a11d62d01d3f2021dd2cd892ffcb47a0b61e1c70a00e4018'
        }

        google_search = GoogleSearch(params)

        response = google_search.get_dict()['search_metadata']['google_url']
        return HttpResponse(json.dumps({'reply': response}), status=status.HTTP_200_OK, charset='utf-8')
