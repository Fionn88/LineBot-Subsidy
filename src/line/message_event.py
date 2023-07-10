from linebot.models import (
    TextMessage, TextSendMessage, PostbackEvent
)
from urls import line_bot_api
from message_handler import *
from data import (
    category,location_dict,category_dict,searchByCode,searchByCategoryAndLocation
)

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