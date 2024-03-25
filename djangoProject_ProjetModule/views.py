import json
import logging

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from djangoProject_ProjetModule.models import Device, CustomUser
from .models import IRCode
from django.urls import reverse  # Add this import statement
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.core.cache import cache
from django.db import transaction

User = get_user_model()
logger = logging.getLogger(__name__)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = CustomUser.objects.create_user(email=email, password=password)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'error': 'Invalid request', 'status': 'error'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        logger.info('Login attempt received for email: %s', email)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            logger.info('Login successful for email: %s', email)

            # Create a new token for the user
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'status': 'ok',
                'token': str(refresh.access_token),
                'user_id': user.id,  # Include the user_id in the response
            })
        else:
            logger.warning('Login failed for email: %s', email)
            return JsonResponse({'error': 'Authentication failed', 'status': 'error'}, status=401)




@csrf_exempt
@login_required
@transaction.atomic
def add_device(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        type = data.get('type')
        deviceLocation = data.get('deviceLocation')
        receiveNotifications = data.get('receiveNotifications')
        image = data.get('image')
        user = request.user

        # Check if a device with the same information already exists
        existing_device = Device.objects.filter(name=name, type=type, deviceLocation=deviceLocation, user=user).first()
        if existing_device:
            return JsonResponse({'error': 'Device already exists', 'status': 'error'}, status=400)

        if name and type and deviceLocation is not None and receiveNotifications is not None and image:
            device = Device.objects.create(name=name, type=type, deviceLocation=deviceLocation, receiveNotifications=receiveNotifications, image=image, user=user)
            device_id = device.device_id  # Get the auto-generated device ID
            user_id=user.id
            response_data = {'status': 'ok', 'device_id': device_id, 'user_id': user_id}
            logger.info(f'Device added: {response_data}')  # Log the response data
            return JsonResponse(response_data)
        else:
            logger.error(f'Error adding device: {data}')  # Log the request data
            return HttpResponseBadRequest(json.dumps({'error': 'Invalid request', 'status': 'error'}), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_devices(request, user_id):
    logger.info(f'get_devices called with user_id: {user_id}')  # Debug message 1
    if request.method == 'GET':
        devices = Device.objects.filter(user_id=user_id)
        logger.info(f'devices: {devices}')  # Debug message 2
        devices_list = [{'id': device.device_id, 'name': device.name, 'type': device.type, 'user_id': user_id} for device in devices]
        logger.info(f'devices_list: {devices_list}')  # Debug message 3
        return JsonResponse({'devices': devices_list}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method', 'status': 'error'}, status=405)







@api_view(['POST'])
def store_ir_codes(request):
    if request.method == 'POST':
        print("Received POST request to store_ir_codes")
        print("Request data:", request.data)

        # Extract device_id and user_id from the request data
        device_id = request.data.get('device_id')
        user_id = request.data.get('user_id')

        if not device_id or not user_id:
            return Response({'error': 'Device ID or User ID is missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the device belongs to the user
        try:
            device = Device.objects.get(device_id=device_id, user_id=user_id)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)

        for functionality, code_list in request.data.items():
            if code_list and functionality != 'device_id' and functionality != 'user_id':
                try:
                    # Convert string to integer
                    print("Functionality:", functionality)
                    print("Code (int):", code_list)
                    ir_code = IRCode.objects.create(functionality=functionality, code=code_list, device=device, user_id=user_id)
                    ir_code.save()
                except ValueError:
                    print(f"Invalid code for functionality: {functionality}. Skipping.")
            elif not code_list:
                print(f"Missing code for functionality: {functionality}")

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def fetch_ir_codes(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id)
        ir_codes = IRCode.objects.filter(device=device).values('code')
        response_data = {
            'device_id': device_id,
            'ir_codes': list(ir_codes)
        }
        return JsonResponse(response_data)
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)