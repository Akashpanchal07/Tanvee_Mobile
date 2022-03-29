from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import login
from common.otp_utils import phone_validator, password_generator, otp_generator
from common.models import User, Profile, Address
from common.serializer.user_serializers import (
    CreateUserSerializer,
    UserSerializer,
    CreateProfileSerializer,
    ProfileSerializer,
    AddressSerializer,
)
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests
import random
from rest_framework.views import APIView


def send_otp(mobile):
    """
    This is an helper function to send otp to session stored phones or
    passed mobile number as argument.
    """

    if mobile:

        key = otp_generator()
        mobile = str(mobile)
        otp_key = str(key)

        # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'

        # result = requests.get(link, verify=False)

        return otp_key
    else:
        return False


"""def send_otp_forgot(mobile):
    if mobile:
        key = otp_generator()
        mobile = str(mobile)
        otp_key = str(key)
        user = get_object_or_404(User, mobile__iexact=mobile)
        if user.first_name:
            name = first_name
        else:
            name = mobile

        # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfgs&templatename=Wisfrags&var1={name}&var2={otp_key}'

        # result = requests.get(link, verify=False)
        # print(result)

        return otp_key
    else:
        return False
"""

############################################################################################################################################################################################
################################################################################################################################################################


"""class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile')
        if mobile_number:
            mobile = str(mobile_number)
            user = User.objects.filter(mobile__iexact=mobile)
            if user.exists():
                return Response({'status': False, 'detail': 'Mobile Number already exists'})
                # logic to send the otp and store the phone number and that otp in table.
            else:
                otp = send_otp(mobile)
                print(mobile, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = MobileOTP.objects.filter(mobile__iexact=mobile)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()

                    else:
                        count = count + 1

                        MobileOTP.objects.create(
                            mobile=mobile,
                            otp=otp,
                            count=count

                        )
                    if count > 7:
                        return Response({
                            'status': False,
                            'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })


                else:
                    return Response({
                        'status': 'False', 'detail': "OTP sending error. Please try after some time."
                    })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail': "I haven't received any mobile number. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password

    '''

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', False)
        otp_sent = request.data.get('otp', False)

        if mobile and otp_sent:
            old = MobileOTP.objects.filter(mobile__iexact=mobile)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status': True,
                        'detail': 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Mobile not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either Mobile or otp was not recieved in Post request'
            })
"""

class Register(APIView):
    '''Takes mobile and otp and creates a new user only if otp was verified and mobile number is new'''

    def post(self, request, *args, **kwargs):


        # password = request.data.get('password', False)
        email = request.data.get('email', False)
        mobile = request.data.get('mobile', False)
        first_name = request.data.get('first_name', False)
        last_name = request.data.get('last_name', False)
        username = request.data.get('username', False)

        check_email = User.objects.filter(email=email).first()
        check_mobile = User.objects.filter(mobile=mobile).first()

        if check_email or check_mobile:
            context = {'message' : 'This Mobile number already exists', 'class' : 'danger' }
            return render(request, context)

        user = User(username=username, email = email, first_name = first_name, last_name = last_name, mobile = mobile)
        user.save()
        # key = otp_generator()
        otp = str(random.randint(9999, 99999))
        # otp_key = str(key)
        profile = Profile(user=user, otp=otp)
        print(profile)
        profile.save()
        # send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return HttpResponse("Otp send your Register Mobile Number sucessfully.")



'''
        if mobile and password:
            mobile = str(mobile)
            user = User.objects.filter(mobile__iexact=mobile)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Mobile Number already have account associated. Kindly try forgot password'})
            else:
                old = MobileOTP.objects.filter(mobile__iexact=mobile)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'mobile': mobile, 'password': password}

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status': True,
                            'detail': 'Congrats, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Mobile number not recognised. Kindly request a new otp with this number'
                    })


        else:
            return Response({
                'status': 'False',
                'detail': 'Either mobile or password was not recieved in Post request'
            })
'''


'''def otp(request):
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    print(context)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)
        profile = Profile.objects.filter(user__mobile=mobile).first()
        # check_user = User.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return HttpResponse("OTP matched, kindly proceed to login")
            # return redirect('cart')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)'''


#
class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    '''


    def post(self, request, *args, **kwargs):
        mobile = request.session['mobile']
        context = {'mobile': mobile}
        print(context)
        otp = request.data.get('otp', False)
        print(otp)
        profile = Profile.objects.filter(user__mobile=mobile).first()

        if otp == profile.otp:
            '''return HttpResponse("OTP matched, Your Otp is Validate")
            # return redirect('cart')'''
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)
        return Response({
            'status': True, 'detail': 'Otp has been matched successfully.'
        })


class ValidateMobileOTP(APIView):
    '''
    This class view takes phone number and it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        mobile = request.session['mobile']
        otp = request.data.get('otp', False)
        profile = Profile.objects.filter(user__mobile=mobile).first()

        if otp == profile.otp:
            # otp = str(otp)
            # otp = profile.otp
            count = 0
            old = Profile.objects.filter(user__mobile=mobile)
            if old.exists():
                count = old.first().count
                old.first().count = count + 1
                old.first().save()

            else:
                count = count + 1

                Profile.objects.create(

                    otp=otp,
                    count=count

                )
            if count > 10:
                return Response({
                    'status': False,
                    'detail': 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                })


        else:
            return Response({
                'status': 'False', 'detail': "OTP sending error. Please try after some time."
            })

        return Response({
            'status': True, 'detail': 'Otp has been matched successfully.'
        })


class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', False)

        profile = Profile.objects.filter(user__mobile=mobile).first()

        if profile is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, context)
            # return render(request, 'login.html', context)

        otp = str(random.randint(9999, 99999))
        profile.otp = otp
        print(profile.otp)
        profile.save()
        # send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return Response(
            {'error': False, 'detail': 'Otp has been send your mobile'}
        )
        # return redirect('login_otp')



    # return render(request, 'login.html')


class LoginOTP(APIView):

    def post(self, request, *args, **kwargs):
        mobile = request.session['mobile']
        context = {'mobile': mobile}
        print(context)
        otp = request.data.get('otp', False)
        profile = Profile.objects.filter(user__mobile=mobile).first()

        if otp == profile.otp:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            # return redirect('cart')
        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': mobile}
            return Response(
                {'status' :True, 'context':context},
            )
            # return render(request, 'login_otp.html', context)

        return Response(
            {"error": False, "message": "User login Successfully."},
            status=status.HTTP_200_OK,
            )
