from linebot.models import (
    TextSendMessage, TemplateSendMessage, QuickReplyButton, ConfirmTemplate, 
    PostbackTemplateAction,URITemplateAction,QuickReply,MessageAction,TextMessage,PostbackEvent
)
from linebot import LineBotApi
import re

import config
from data import (
    category,location_dict,category_dict,searchByCode,searchByCategoryAndLocation
)

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

        elif messages == '問題回報':

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
                    sendList(event,user_click_category,user_click_location,result)
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
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資料庫發生錯誤，請聯絡管理員!\n信箱：'+config.TEAM_EMAIL))
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
        if re.match('.*尚未填寫申辦說明', result[6]) or len(result[6]) == 1:
            message.append(TextSendMessage('目前相關單位還沒填寫詳情，請直接點選查看更多至網頁查看更詳細資訊。'))
        else:
            message.append(TextSendMessage(f'{result[6]}'))
        
        message.append(TemplateSendMessage(
            alt_text = '津貼條件',
            template = ConfirmTemplate(
                text='您還可以看看：',
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
         text = '請問您今天想要查詢哪個類別的津貼呢?'
    elif typeButton == "selectLocation":
        text = '請問您的戶籍地是台灣哪區呢?'
    elif typeButton == "selectBigLocation":
        text = '請問您的戶籍地是哪個縣市呢?'
    for item in listData:
        actionsList.append(QuickReplyButton(action=MessageAction(label=item,text=item,data=f'action={typeButton},data={item}')))
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
    if re.match('.*尚未填寫申辦說明', result[5]) or len(result[5]) == 1:
        message.append(TextSendMessage(text='目前相關單位還沒填寫詳情，請直接點選查看更多至網頁查看更詳細資訊。'))
    else:
        message.append(TextSendMessage(text=result[5]))
    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
        print("=========================")
        print("Exception: ",e)
        print("=========================")

def sendList(event,category,location,result):
    message = []
    text = ""
    for index,list in enumerate(result):
        if index == len(result) - 1:
            text += list[0]+" "+list[1]
        else:
            text += list[0]+" "+list[1]+"\n"
    message.append(TextSendMessage(text=text))
    message.append(TextSendMessage(f'以上是在中央政府及{location}的{category}相關的津貼ID列表，請在訊息視窗輸入津貼前面的數字(ID)查詢津貼的詳情'))

    try:
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
        print("=========================")
        print("Exception: ",e)
        print("=========================")