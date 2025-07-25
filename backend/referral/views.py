from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache
import random
import time

User = get_user_model()

class PhoneAuthView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Укажите номер телефона'}, status=status.HTTP_400_BAD_REQUEST)
        code = f'{random.randint(1000, 9999)}'
        cache.set(f'auth_code_{phone}', code, timeout=300) # 5 минут
        time.sleep(1.5)
        return Response({'message': 'Код отправлен (имитация)', 'phone': phone}, status=status.HTTP_200_OK)

class CodeAuthView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        if not phone or not code:
            return Response({'error': 'Укажите номер и код'}, status=status.HTTP_400_BAD_REQUEST)
        real_code = cache.get(f'auth_code_{phone}')
        if code != real_code:
            return Response({'error': 'Неверный или просроченный код'}, status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(phone=phone, defaults={"username": phone})
        return Response({'message': 'Успешная авторизация', 'is_new': created, 'user_id': user.id}, status=status.HTTP_200_OK)
