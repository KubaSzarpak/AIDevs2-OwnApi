import openai
import dotenv
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Create your views here.


dotenv.load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY', default='')

CLIENT = openai.Client(api_key=OPENAI_API_KEY)


class Chatbot(APIView):
    def post(self, request):
        question = self.request.data.get('question', '')
        if not question:
            return Response({'message': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

        response = CLIENT.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': question}
            ]
        ).choices[0].message.content

        return Response({'reply': response}, status=status.HTTP_200_OK)
