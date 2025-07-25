from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache
import random
import time
from auth.jwt_django import encode_jwt
from django.views import View
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from auth.jwt_django import decode_jwt

User = get_user_model()

class HomeView(View):
    def get(self, request):
        return render(request, 'referral/home.html')

class PhoneAuthView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'error': 'Укажите номер телефона'}, status=status.HTTP_400_BAD_REQUEST)
        code = f'{random.randint(1000, 9999)}'
        cache.set(f'auth_code_{phone}', code, timeout=300) # 5 минут
        time.sleep(1.5)
        return Response({'message': f'Код отправлен (имитация): {code}', 'phone': phone}, status=status.HTTP_200_OK)

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
        # Генерируем JWT-токен
        token = encode_jwt({"user_id": user.id, "phone": user.phone})
        resp = Response({'message': 'Успешная авторизация', 'is_new': created, 'user_id': user.id}, status=status.HTTP_200_OK)
        resp.set_cookie('jwt', token, httponly=True, samesite='Lax')
        return resp

class ProfileView(View):
    def get_user_from_jwt(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            payload = decode_jwt(token)
            user = User.objects.filter(id=payload.get('user_id')).first()
            return user
        except Exception:
            return None

    def get(self, request):
        user = self.get_user_from_jwt(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        invited_users = User.objects.filter(activated_invite_code=user.invite_code)
        invited_phones = [u.phone for u in invited_users]
        return JsonResponse({
            'phone': user.phone,
            'invite_code': user.invite_code,
            'activated_invite_code': user.activated_invite_code,
            'invited_users': invited_phones
        })

    def post(self, request):
        user = self.get_user_from_jwt(request)
        if not user:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        if user.activated_invite_code:
            return JsonResponse({'error': 'Инвайт-код уже был активирован', 'activated_invite_code': user.activated_invite_code}, status=400)
        import json
        data = json.loads(request.body)
        code = data.get('invite_code')
        if not code:
            return JsonResponse({'error': 'Не передан инвайт-код'}, status=400)
        if code == user.invite_code:
            return JsonResponse({'error': 'Нельзя активировать свой собственный инвайт-код'}, status=400)
        inviter = User.objects.filter(invite_code=code).first()
        if not inviter:
            return JsonResponse({'error': 'Инвайт-код не найден'}, status=404)
        user.activated_invite_code = code
        user.save()
        return JsonResponse({'message': 'Инвайт-код успешно активирован', 'activated_invite_code': code})
