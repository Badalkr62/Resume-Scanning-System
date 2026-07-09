import random

def generateOTP():

    otp=random.randint(100000,999999)

    return str(otp)