#!/usr/bin/python
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(10, GPIO.IN)

# Create your views here.
def index(request):
    led = (request.POST.get('led', 'Stop' ))
    led_status = 'Turned off'

    if led=='Start':
        led_status = 'Turned on'
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(27,GPIO.HIGH)
    else:
        led_status = 'Turned off'
        GPIO.output(27,GPIO.LOW)
        GPIO.output(17,GPIO.LOW)
    return render(request, 'Raspberry/index.html',{'led_status': led_status})
