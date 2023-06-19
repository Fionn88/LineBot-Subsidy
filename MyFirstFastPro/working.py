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
support = {"育兒津貼": ["育有未滿2歲兒童育兒津貼","桃園市生育津貼","農民健康保險生育給付申辦"]}
supportFullInfo = {"育有未滿2歲兒童育兒津貼": ["實際年齡未滿2歲的我國籍兒童，且請領當時符合下列情形者：","一、 完成出生登記或初設戶籍登記。","二、 未經政府公費安置收容。","三、未接受公共化或準公共托育服務。"]}
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

@handler.add(MessageEvent, message=(TextMessage))
def handling_message(event):
    if isinstance(event.message, TextMessage):
        messages = event.message.text      
        getDict = support.get(messages)
        sendButton(event,getDict)


@handler.add(PostbackEvent)        
def handle_postback(event):
    if isinstance(event, PostbackEvent):
        try:
            backdata = event.postback.data.split('=')[1]
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能!'))
        else:
            supportFullInfoList = supportFullInfo.get(backdata)
            if supportFullInfoList == None:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            else:
                name = backdata
                sendConfirm(event,name,supportFullInfoList)

def sendConfirm(event,name,listItem):
    titleMessage = ''
    message = []
    for index,value in enumerate(listItem):
        if index == len(listItem) -1 :
            titleMessage += value
        else:
            titleMessage += value
            titleMessage += '\n'
            
    try:
        message.append(TextSendMessage('您點選了：'+name))
        message.append(TemplateSendMessage(
            alt_text = '津貼條件',
            template = ConfirmTemplate(
                text=f'{titleMessage}',
                actions=[
                    PostbackTemplateAction(
                        label='符合條件',
                        data=f'{name}'
                    ),
                    PostbackTemplateAction(
                        label='不符合條件',
                        data=f'{name}'
                    )
                ]
            )
        ))
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendYes(event):
    try:
        message = TextSendMessage(
            text = '感謝您的購買，\n我們會盡快寄出商品',
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))



def sendButton(event,listItem):
    actionsList = []
    for item in listItem:
        actionsList.append(PostbackTemplateAction(label=item,data=f'action={item}'))
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