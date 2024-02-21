
from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('743369464D3573444D664434577550373262686950554C6436337A584C6631366D767439634C384646664D3D')
        params = {
            'sender': '',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': 'code : {code}',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)


