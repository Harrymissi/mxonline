_auther_ = 'Harry'
_date_ = '2/1/2018 9:56 PM'

from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from untitled1.settings import EMAIL_FROM



def random_str(randomlength=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type=send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type=="register":
        email_title = 'mxonline register verification link'
        email_body = 'please click link below to activate your account: http://127.0.0.1:8000/active/{0}'.format(code)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:  #发送成功为true
            pass

    elif send_type == "forget":
        email_title =   'password reset'
        email_body ='please click link below to reset your password: http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:  # 发送成功为true
            pass


    elif send_type == "update_email":
        email_title = 'email reset'
        email_body = 'code to reset your email: {0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:  # 发送成功为true
            pass
