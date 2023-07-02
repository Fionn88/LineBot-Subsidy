from linebot.models import (
    TextMessage, TextSendMessage, TemplateSendMessage, QuickReplyButton, ConfirmTemplate, 
    PostbackTemplateAction, PostbackEvent,URITemplateAction,QuickReply
)
from linebot import LineBotApi

from data import (
    category,searchByName,searchByCategory
)

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)

# 文字傳入執行
def handle_message(event) -> None:
    if isinstance(event.message, TextMessage):
        messages = event.message.text.strip()
        if messages == '津貼查詢':
            sendQuickreply(event,category,'selectCategory')
        elif messages == '個人資訊':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        elif messages in category:
            print("===============")
            print("Do SomeThing SELECT name WHERE category = ? in data.py")
            print("===============")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料庫目前未準備好分類，敬請期待新功能！'))
            # result = searchByCategory(messages)
            # if result == None:
            #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='沒有此津貼\n請輸入「津貼查詢」，或是完整津貼名稱。'))
            # elif result == 'Error':
            #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料庫發生錯誤，請聯絡管理員!\n信箱：@gmail.com'))
            # else:
            #     sendQuickreply(event,result,'selectItem')
        else:
            result = searchByName(messages)
            if result == None:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='沒有此津貼\n請輸入「津貼查詢」，或是完整津貼名稱。'))
            elif result == 'Error':
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料庫發生錯誤，請聯絡管理員!\n信箱：@gmail.com'))
            else:
                sendConfirm(event,result,'sendConfirm')
            

# 按按鈕後回傳資訊執行 
def handle_postback(event) -> None:
    if isinstance(event, PostbackEvent):
        try:
            backdataSplit = event.postback.data.split(',')
            backtype = backdataSplit[0].split('=')[1]
            backdata = backdataSplit[1].split('=')[1]
            print("=========================")
            print('backtype: ',backtype)
            print('backdata: ',backdata)
            print("=========================")
        except Exception as e:
            print("=========================")
            print("Exception: ",e)
            print("=========================")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))
        else:
            if backtype == 'sendConfirm':
                result = searchByName(backdata)
                sendContent(event,result)
                # listSupport = support.get(backdata)
                # sendQuickreply(event,listSupport,'selectSupportItem')
            # elif backtype == 'selectItem':
                # sendConfirm(event,result,'sendConfirm')
                    

def sendConfirm(event,result,typeButton):
    message = []
    try:
        message.append(TextSendMessage(f'以下是{result[1]}的申辦資格'))
        message.append(TextSendMessage(f'{result[6]}'))
        message.append(TemplateSendMessage(
            alt_text = '津貼條件',
            template = ConfirmTemplate(
                text='請選擇：',
                actions=[
                    PostbackTemplateAction(
                        label='補助內容',
                        data=f'action={typeButton},data={result[1]}'
                    ),
                    URITemplateAction(
                        label='查看更多',
                        uri=f'{result[4]}'
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
    for item in listItem:
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

def sendContent(event,result):
    message = []
    message.append(TextSendMessage(text=result[3]))
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print(e)