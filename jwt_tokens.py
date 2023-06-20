import jwt
import time
from flask_restful import request



key = 'kekburger'
lifeTimeDuration = 10



def createJWT(login, password):
    
    payload_data = {
        "login" : login,
        "password" : password,
        "creation_time" : time.time()
    }   
        
    token = jwt.encode (
        payload_data,
        key
    )

    return token



def verifyToken(token):
    decoded = ''
    try:
        decoded = jwt.decode(token, key, algorithms="HS256")
        if decoded["creation_time"] + lifeTimeDuration < time.time():
            return {"result" : "Time is over. Log in again."} 
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as exc:
        print(str(exc))
        return {"result" : "Not verified"}

    return {"result" : "Verified", "info" : {"login" : decoded["login"]}}



def verify(role):
    cookie_token = request.cookies.get("my_token")
    if (cookie_token == None):
        return {"INFO" : "Please authenticate"}

    cookie_role = request.cookies.get("my_role")
    cookie_name = request.cookies.get("my_name")
    verifyResult = verifyToken(cookie_token)
    if verifyResult["result"] == "Verified":
        verifyResult["info"]["role"] = cookie_role
        verifyResult["info"]["name"] = cookie_name
        if role == "" or role == cookie_role:
            return verifyResult
        else:
            return {"INFO" : "You have no rights for this operation"}
    else:
        return {"INFO" : verifyResult["result"]}
