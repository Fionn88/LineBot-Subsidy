from linebot.models import (
    TextMessage, TextSendMessage, TemplateSendMessage, QuickReplyButton, ConfirmTemplate, 
    PostbackTemplateAction, PostbackEvent,URITemplateAction,MessageAction,QuickReply
)
from linebot import LineBotApi

from data import (
    supportFullInfo,support,supportContent,supportURL,category,searchByName
)

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

# 文字傳入執行
def handle_message(event) -> None:
    if isinstance(event.message, TextMessage):
        messages = event.message.text
        print(messages)
        if messages == '津貼查詢':
            sendQuickreply(event,category,'selectCategory')
        elif messages == '個人資訊':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        else:
            print(messages)
            result = searchByName(messages)
            print(result)
            if result == None:
                print('===================')
                print('istSupport == None')
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='沒有此津貼\n請輸入「津貼查詢」，或是完整津貼名稱。'))
            elif result == 'Error':
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料庫 Internal Error'))
            else:
                print(result)
                # sendContent(event,listSupport,'selectSupportClass')
            

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
            if backtype == 'selectCategory':
                listSupport = support.get(backdata)
                sendQuickreply(event,listSupport,'selectSupportItem')
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


def sendQuickreply(event,listItem, typeButton):
    actionsList = []
    # print('===================================')
    # print('sendButton')
    print(listItem)
    for item in listItem:
        # actionsList.append(QuickReplyButton(label=item,text=item,data=f'action={typeButton},data={item}'))
        actionsList.append(QuickReplyButton(action=PostbackTemplateAction(label=item,text=item,data=f'action={typeButton},data={item}')))
    print(actionsList)
    try:
        message = TextSendMessage(
            text = '津貼項目選擇',
            quick_reply=QuickReply(
              items=actionsList
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