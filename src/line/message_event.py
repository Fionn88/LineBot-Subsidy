from linebot.models import (
    TextMessage, TextSendMessage, TemplateSendMessage, QuickReplyButton, ConfirmTemplate, 
    PostbackTemplateAction, PostbackEvent,URITemplateAction,QuickReply
)
from linebot import LineBotApi

from data import (
    category,location_dict,category_dict,searchByCode,searchByCategoryAndLocation
)

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
user_click_category = None  
user_click_location = None

# 文字傳入執行
def handle_message(event) -> None:
    global user_click_category
    global user_click_location

    location_raw_list = list(location_dict.values())
    location_extract_list = [value for sublist in location_raw_list for value in sublist]

    if isinstance(event.message, TextMessage):
        messages = event.message.text.strip()

        if messages == '津貼查詢':

            sendQuickreply(event, category,'selectCategory')

        elif messages == '個人資訊':

            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='敬請期待新功能！'))

        elif messages in category:

            user_click_category = messages
            sendQuickreply(event,list(location_dict),'selectBigLocation')
            
        elif messages in list(location_dict) :

            location_list = location_dict.get(messages)
            sendQuickreply(event,location_list,'selectLocation')

        elif messages in location_extract_list:

            user_click_location = messages
            if not user_click_category:
                sendQuickreply(event, category,'selectCategory')
            else:
                result = searchByCategoryAndLocation(category_dict.get(user_click_category),user_click_location)
                if result:
                    sendList(event,result)
                else:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='目前沒有您選取的條件津貼，如想詳細查詢請到E政府'))
                

        else:
            try:
                _ = int(messages)
            except ValueError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入津貼ID查詢津貼'))
            else:
                result = searchByCode(messages)
                if result == None:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='沒有此津貼ID'))
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
            print('postbackType: ',backtype)
            print('postbackData: ',backdata)
            print("=========================")

        except Exception as e:

            print("=========================")
            print("Exception: ",e)
            print("=========================")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤，請聯絡管理員!\n信箱：@gmail.com'))

        else:

            if backtype == 'sendConfirm':
                result = searchByCode(backdata)
                sendContent(event,result)
                    

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
                        data=f'action={typeButton},data={result[0]}'
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
        print("=========================")
        print("Exception: ",e)
        print("=========================")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def sendQuickreply(event, listData ,typeButton):
    actionsList = []
    if typeButton == "selectCategory":
         text = '津貼類別選擇'
         for item in listData:
             actionsList.append(QuickReplyButton(action=PostbackTemplateAction(label=item,text=item,data=f'action={typeButton},data={item}')))
    elif typeButton == "selectLocation" or typeButton == "selectBigLocation":
        text = '津貼承辦單位地點選擇'
        for item in listData:
             actionsList.append(QuickReplyButton(action=PostbackTemplateAction(label=item,text=item,data=f'action={typeButton},data={item}')))
    try:
        message = TextSendMessage(
            text = text,
            quick_reply=QuickReply(
              items=actionsList
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        print("=========================")
        print("Exception: ",e)
        print("=========================")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendContent(event,result):
    message = []
    print(result)
    message.append(TextSendMessage(text=result[5]))
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
        print("=========================")
        print("Exception: ",e)
        print("=========================")

def sendList(event,result):
    message = []
    text = ""
    message.append(TextSendMessage('以下是您欲查詢的津貼補助，請輸入津貼ID查詢津貼'))
    for index,list in enumerate(result):
        if index == len(result) - 1:
            text += list[0]+" "+list[1]
        else:
            text += list[0]+" "+list[1]+"\n"
    message.append(TextSendMessage(text=text))
        
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
        print("=========================")
        print("Exception: ",e)
        print("=========================")