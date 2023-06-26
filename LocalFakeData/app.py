from fastapi import FastAPI, Request, HTTPException
from urllib.parse import urlparse

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage, ButtonsTemplate, MessageTemplateAction,ConfirmTemplate,PostbackTemplateAction,PostbackEvent
)

# Line Bot config
accessToken = "your access token to line bot which get from line biz"
secret = "your secret token to access line bot webhook get from line developer"


app = FastAPI()
support = {"育兒津貼": ["育有未滿2歲兒童育兒津貼","桃園市生育津貼","農民健康保險生育給付申辦"],
"老年給付": ["勞保老年給付申辦（個人申辦用）","勞保老年給付申辦（個人申辦用）"]}
supportFullInfo = {"育有未滿2歲兒童育兒津貼": ["實際年齡未滿2歲的我國籍兒童，且請領當時符合下列情形者：","一、 完成出生登記或初設戶籍登記。","二、 未經政府公費安置收容。","三、未接受公共化或準公共托育服務。"],
"桃園市生育津貼":["一、新生兒符合下列各款規定之一，其設籍本市連續達一年以上，且申請時仍設籍本市之父或母，得申請本要點津貼：","(一)新生兒在本市各戶所辦理出生登記。","(二)非於國內出生之新生兒，返國後在本市各戶所辦理初設戶籍登記。","二、前項設籍期間之計算，以最後遷入本市之日起，算至新生兒出生之日止。","新生兒之父母因死亡、行蹤不明或受監護宣告致無法提出申請者，得由同戶籍之監護人或三親等以內血親提出申請。","申請本要點津貼者，應於新生兒出生之次日起六個月內提出申請。"],
"農民健康保險生育給付申辦":["一、請領資格：","(一) 被保險人或其配偶參加農保後分娩者。","(二) 被保險人或其配偶參加農保後早產者。","※【早產】定義：為胎兒產出時妊娠週數20週以上（含140天），但未滿37週者（不含259天）。如妊娠週數不明確時，可採胎兒產出時體重超過500公克但未滿2,500公克為判斷標準。","二、給付標準：","生育給付標準，依下列各款辦理：","(一) 分娩或早產者，按其事故發生當月之投保金額一次給與 3 個月。","(二) 雙生以上者，比例增給。","※ 舊法給付：110年12月24日農保條例修正施行，故110年12月23日（含當日）前流產、早產或分娩，符合加保年資條件者，得依舊法申請生育給付。"]}
supportContent = {"育有未滿2歲兒童育兒津貼":["發放金額：","一、第1名子女：每人每月5,000元。","二、第2名子女：每人每月6,000元。","三、第3名(含)以上子女：每人每月7,000元。所稱第 2 名或第 3 名(含)以上子女，指戶籍登記為同一母或父，依出生年月日排序計算為第 2 名或第 3 名以上之子女。"],
"桃園市生育津貼":["一、政策說明","(一)為感謝並慰勞新生兒家庭生育辛勞及紓緩育兒負擔，本府於103年12月25日升格為直轄市後，整合統一，自104年4月1日起開辦生育津貼，以鼓勵生育，提高生育率。","一，自104年4月1日起開辦生育津貼，以鼓勵生育，提高生育率。"," (二)為達簡政便民之效能，自104年5月1日起，啟動多元窗口，除向戶政事務所申請外，另開放各區公所（社會課）受理生育津貼申請，以提供市民近便服務。",
"二、發放金額","適用舊制新生兒出生日期為111年12月24日(含當日)以前。","每名新生兒發放新臺幣(以下同)3萬元。","雙胞胎每名新生兒發放3萬5,000元。","三胞胎每名新生兒發放4萬5,000元。"
,"適用新制新生兒出生日期為111年12月25日(含當日)以後。","第一名子女發放3萬元。","第二名子女發放4萬元。","第三名子女(含)以上，每名發放5萬元","倘若為多胞胎，則另加碼補助，每名1萬元。","*子女排序之計算，以同一母親所生活產胎兒之次序，並以申請時已完成申報戶籍登記為準。"]}
supportURL = {"桃園市生育津貼":"https://www.gov.tw/News3_Content.aspx?n=2&s=669382","育有未滿2歲兒童育兒津貼":"https://www.gov.tw/News3_Content.aspx?n=2&s=375315","農民健康保險生育給付申辦":"https://www.gov.tw/News3_Content.aspx?n=2&s=389481"}
line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler(secret)



@app.post("/")
async def echoBot(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

# 文字傳入執行
@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    if isinstance(event.message, TextMessage):
        messages = event.message.text      
        listSupport = support.get(messages)
        if messages == '津貼查詢':
            sendButton(event,list(support),'selectSupport')
        elif messages == '個人資訊':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        else:
            sendContent(event,listSupport,'selectSupportClass')
        

# 按按鈕後回傳資訊執行
@handler.add(PostbackEvent)        
def handle_postback(event):
    if isinstance(event, PostbackEvent):
        try:
            backdataSplit = event.postback.data.split(',')
            backtype = backdataSplit[0].split('=')[1]
            backdata = backdataSplit[1].split('=')[1]
            print('backtype',backtype)
            print('backdata',backdata)
        except Exception as e:
            print(e)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        else:
            if backtype == 'selectSupport':
                listSupport = support.get(backdata)
                sendButton(event,listSupport,'selectSupportItem')
            elif backtype == 'selectSupportItem':
                supportFullInfoList = supportFullInfo.get(backdata)
                if supportFullInfoList == None:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
                else:
                    sendConfirm(event,backdata,supportFullInfoList,'sendConfirm')
            elif backtype == 'sendConfirm':
                supportContentList = supportContent.get(backdata)
                if supportContentList == None:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
                else:
                    sendContent(event,supportContentList)
                
                    

def sendConfirm(event,name,listItem,typeButton):
    titleMessage = ''
    message = []
    for index,value in enumerate(listItem):
        if index == len(listItem) -1 :
            titleMessage += value
        else:
            titleMessage += value
            titleMessage += '\n'
            
    try:
        message.append(TextSendMessage(f'以下是{name}的申辦資格'))
        message.append(TemplateSendMessage(
            alt_text = '津貼條件',
            template = ConfirmTemplate(
                text=f'{titleMessage}',
                actions=[
                    PostbackTemplateAction(
                        label='補助內容',
                        data=f'action={typeButton},data={name}'
                    ),
                    URITemplateAction(
                        label='查看更多',
                        uri=f'{supportURL.get(name)}'
                    )
                ]
            )
        ))
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def sendButton(event,listItem, typeButton):
    actionsList = []
    # print('===================================')
    # print('sendButton')
    print(listItem)
    for item in listItem:
        actionsList.append(PostbackTemplateAction(label=item,data=f'action={typeButton},data={item}'))
    try:
        message = TemplateSendMessage(
            alt_text = '津貼項目選擇',
            template = ButtonsTemplate(
                # thumbnail_image_url='https://i.imgur.com/pRdaAmS.jpg',
                title='津貼項目',
                text='請選擇：',
                actions=actionsList
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print(e)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendContent(event,listItem):
    textMessage = ''
    message = []
    for index,value in enumerate(listItem):
        if index == len(listItem) -1 :
            textMessage += value
        else:
            textMessage += value
            textMessage += '\n'
    # print('===================================')
    # print('sendContent')
    print(listItem)
    message.append(TextSendMessage(text=textMessage))
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print(e)