import requests,uuid,sys
print("ClientUUID get tool")

phone_number=(input("電話番号を入力してください。\n>>"))
password=input("パスワードを入力してください。\n>>")
session = requests.Session()
try:
    aaafdsa=int(phone_number)
except:
    print("Error")
    sys.exit()
#リンクの情報を取得
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept' : 'application/json, text/plain, */*',
    'Content-Type' : 'application/json'
}
                
set_uuid=str(uuid.uuid4())
payload = {
    "scope":"SIGN_IN",
    "client_uuid":f"{set_uuid}",
    "grant_type":"password",
    "username":phone_number,
    "password":password,
    "add_otp_prefix": True,
    "language":"ja"
}




aaa=session.post("https://www.paypay.ne.jp/app/v1/oauth/token",headers=headers,json=payload)
eee=aaa.json()
print(eee)
try:
    eee=(eee["access_token"])
except:
        if eee["response_type"]=="ErrorResponse":
            print("失敗しました。電話番号かパスワードが間違っている可能性があります。")
            sys.exit()
        else:
            otpid=(eee["otp_reference_id"])
            otp_pre=(eee["otp_prefix"])
            #print(otpid)
            #print(otp_pre)
            print(f"{phone_number}に認証番号が送信されました。")
            otp_number=input(f"認証番号を入力してください。\n>>")
            try:
                fdhdfhjfdhj=int(otp_number)
            except:
                print("それは数字ではありません。\n4桁の数字を入力してください。")
                sys.exit()
            otp_bango=otp_number



                            
            payload = {
                "scope":"SIGN_IN",
                "client_uuid":f"{set_uuid}",
                "grant_type":"otp",
                "otp_prefix": otp_pre,
                "otp":otp_bango,
                "otp_reference_id":otpid,
                "username_type":"MOBILE",
                "language":"ja"
            }
            aaa=session.post("https://www.paypay.ne.jp/app/v1/oauth/token",headers=headers,json=payload)
            eee=aaa.json()
            print(eee)
            try:
                if eee["response_type"]=="ErrorResponse":
                    print("失敗しました。認証番号が間違っている可能性があります。")
                    sys.exit()
            except:
                None
            print("電話番号:"+phone_number)
            print("パスワード:"+password)
            print("Client_UUID↓")
            print(set_uuid)