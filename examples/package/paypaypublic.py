import requests,datetime
import package.config_load as col



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept' : 'application/json, text/plain, */*',
    'Content-Type' : 'application/json'
    }

ppc=col.load()
client_uuid=ppc["client_uuid"]
phone_number=ppc["phone_number"]
pp_password=ppc["password"]



def start(code,passcode1):
    #sessionを開始
    session = requests.Session()
    

    

    #リンクの情報を取得
    getp2pinfo={
    "Accept":"application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }

    aaaaaa=session.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={code}&client_uuid={client_uuid}",headers=getp2pinfo)
    dataf=aaaaaa.json()

    #orderStatusがsuccess(受け取り済)だったらreturnする、さらに、SUCCESSかどうかすら確認できなかったらリンクが存在しないってことだからreturnする。
    try:
        if (dataf["payload"]["orderStatus"]) == "SUCCESS":
            return("SUCCESS")
    except:
        return("Cannot find P2P link")



    #------------------------------------------------------



    #-------------------login----------------------------

    payload = {
        "scope":"SIGN_IN",
        "client_uuid":f"{client_uuid}",
        "grant_type":"password",
        "username":phone_number,
        "password":pp_password,
        "add_otp_prefix": True,
        "language":"ja"
        }




    aaa=session.post("https://www.paypay.ne.jp/app/v1/oauth/token",headers=headers,json=payload)
    eee=aaa.json()
    #access_tokenが取得できた->正しくログインできた
    #取得できなかった->正しくログインできなかった
    #               ->レスポンスを出力
    try:
      eee=(eee["access_token"])
    except:
        try:
            otpid=(eee["otp_reference_id"])#これで取得できちゃってたらOTPのSMS飛んでる->OTP認証済のclient uuidを使用することでOTPをbypass
            print("OTP認証が完了したclient uuidを使用してください。")
            return
        except:
            print(eee)
            return
    #--------------------------------------------------------------

    utcnowtime=str(datetime.datetime.utcnow().isoformat("T","seconds"))

    sendmoneylink_data = {"verificationCode":f"{code}",#関数の引数から
                        "client_uuid":f"{client_uuid}",#変数から
                        "passcode":f"{passcode1}",#関数の引数から
                        "requestAt":f"{utcnowtime}Z",#67行目から(requestAtは必須)
                        "requestId":dataf["payload"]["message"]["data"]["requestId"],#getP2PLinkInfoから
                        "orderId":dataf["payload"]["message"]["data"]["orderId"],#getP2PLinkInfoから
                        "senderMessageId":dataf["payload"]["message"]["messageId"],#getP2PLinkInfoから
                        "senderChannelUrl":dataf["payload"]["message"]["chatRoomId"],#getP2PLinkInfoから
                        "iosMinimumVersion":"2.55.0",#一応書く
                        "androidMinimumVersion":"2.55.0"#一応書く
                        }
    #ヘッダーは一応検知対策
    sendmoneylink_head={
    "Accept":"application/json, text/plain, */*",
    "Content-Type":"application/json",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }

    
    response = session.post('https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink', json=(sendmoneylink_data), headers=sendmoneylink_head)
    print(response.json())
    kessai=response.json()
    if kessai["header"]["resultMessage"]=="Specific Error with half sheet":
        return("パスコードが違います")#パスコードが違った場合、２日ほど後に送金したお金が返ってくる
    print("orderStatus:"+dataf["payload"]["orderStatus"])
    if dataf["payload"]["orderStatus"] =="REJECTED":#辞退済なら受け取り済ということにしとく(抜き取り対策)
        return "SUCCESS"
    print("displayName:"+dataf["payload"]["sender"]["displayName"])#送金者の名前
    print("photoUrl:"+dataf["payload"]["sender"]["photoUrl"])#送金者のアイコン
    print("money:"+str(dataf["payload"]["pendingP2PInfo"]["amount"]))#金額
    disn=dataf["payload"]["sender"]["displayName"]#送金者の名前
    phurl=(dataf["payload"]["sender"]["photoUrl"])#送金者のアイコン
    amount=str(dataf["payload"]["pendingP2PInfo"]["amount"])#金額
    cp=dataf["payload"]["orderStatus"]#一応orderStatusを変数に入れただけ
    return([disn,phurl,amount])
    #リスト形式で[送金者の名前,アイコン,金額]を返す





def check_pcode(code):#パスワードがあるかないか確認

    #リンクの情報を取得
    getp2pinfo={
    "Accept":"application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }
    aaaaaa=requests.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={code}&client_uuid={client_uuid}",headers=getp2pinfo)
    dataf=aaaaaa.json()
    try:
        if (dataf["payload"]["orderStatus"]) == "SUCCESS":
            return("SUCCESS")
    except:
        return("Cannot find P2P link")
    if (dataf["payload"]["pendingP2PInfo"]["isSetPasscode"])==True:
        return('パスワード付き')
    if (dataf["payload"]["pendingP2PInfo"]["isSetPasscode"])==False:
        return('パスワード無し')



def check_price(code):

    #リンクの情報を取得
    getp2pinfo={
    "Accept":"application/json, text/plain, */*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }
    aaaaaa=requests.get(f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo?verificationCode={code}&client_uuid={client_uuid}",headers=getp2pinfo)
    dataf=aaaaaa.json()
    return(dataf["payload"]["pendingP2PInfo"]["amount"])#金額を返す
