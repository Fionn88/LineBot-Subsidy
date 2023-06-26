from linebot.models import (
    TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, ConfirmTemplate, PostbackTemplateAction, PostbackEvent,URITemplateAction
)
from linebot import LineBotApi

from data import (
    supportFullInfo,support,supportContent,supportURL
)

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

# 文字傳入執行
def handle_message(event) -> None:
    if isinstance(event.message, TextMessage):
        messages = event.message.text      
        listSupport = support.get(messages)
        if messages == '津貼查詢':
            sendButton(event,list(support),'selectSupport')
        elif messages == '個人資訊':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        else:
            if listSupport == None:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='沒有此津貼\n請輸入「津貼查詢」，或是完整津貼名稱。'))
            else:
                sendContent(event,listSupport,'selectSupportClass')
            

# 按按鈕後回傳資訊執行 
def handle_postback(event) -> None:
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
    except Exception as e:
        print(e)
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