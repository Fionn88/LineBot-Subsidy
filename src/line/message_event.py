from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    QuickReplyButton, ConfirmTemplate,
    PostbackTemplateAction, URITemplateAction,
    QuickReply, MessageAction, TextMessage, PostbackEvent
)
from linebot import LineBotApi
import re
import logging

import config
from data import (
    category, location_dict,
    category_dict, searchByCode, searchByCategoryAndLocation
)

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
user_click_category = None
user_click_location = None
serviceVersion = 'v1.0.4'

FORMAT = '%(asctime)s %(filename)s %(levelname)s:%(message)s'
# 可變變數
logging.basicConfig(level=logging.INFO, format=FORMAT)


# 文字傳入執行
def handle_message(event) -> None:
    global user_click_category
    global user_click_location

    location_raw_list = list(location_dict.values())
    location_extract_list = [value for sublist in location_raw_list
                             for value in sublist]

    if isinstance(event.message, TextMessage):
        messages = event.message.text.strip()

        if messages == '津貼查詢':

            sendQuickreply(event, list(location_dict), 'selectLocation')

        elif messages == '個人資訊':

            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text='敬請期待新功能！'))

        elif messages in category:

            user_click_category = messages
            if not user_click_location:
                sendQuickreply(event, category, 'selectCategory')
            else:
                result = searchByCategoryAndLocation(
                    category_dict.get(user_click_category),
                    user_click_location)
                if result == "Error":
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage(text='資料庫發生錯誤， \
                                                               請聯絡管理員!\n 信箱：' +
                                                               config.
                                                               TEAM_EMAIL))
                elif result:
                    sendList(event, user_click_category,
                             user_click_location, result)
                else:
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage
                                               (text='目前沒有您選取的條件津貼， \
                                                如想詳細查詢請到E政府'))

        elif messages in list(location_dict):

            location_list = location_dict.get(messages)
            sendQuickreply(event, location_list, 'selectBigLocation')

        elif messages in location_extract_list:

            user_click_location = messages
            sendQuickreply(event, category, 'selectCategory')

        elif messages == '服務版本資訊':
            line_bot_api.reply_message(event.reply_token, TextSendMessage
                                       (text=f'服務版本為 {serviceVersion}， \
                                        具體更新詳細內容請至： \
                                        https://github.com/Fionn88 \
                                        /LineBot-Subsidy/releases'))

        else:
            try:
                _ = int(messages)
            except ValueError:
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text='請輸入津貼ID查詢津貼'))
            else:
                result = searchByCode(messages)
                match result:
                    case None:
                        line_bot_api.reply_message(event.reply_token,
                                                   TextSendMessage(
                                                       text='沒有此津貼ID'
                                                       ))
                    case "Error":
                        line_bot_api.reply_message(event.reply_token,
                                                   TextSendMessage(
                                                       text='資料庫發生錯誤， \
                                                            請聯絡管理員!\n 信箱：' +
                                                            config.
                                                            TEAM_EMAIL
                                                        ))
                    case _:
                        sendConfirm(event, result, 'sendConfirm')


# 按按鈕後回傳資訊執行
def handle_postback(event) -> None:

    if isinstance(event, PostbackEvent):
        try:

            backdataSplit = event.postback.data.split(',')
            backtype = backdataSplit[0].split('=')[1]
            backdata = backdataSplit[1].split('=')[1]
            logging.info('postbackType: ', backtype)
            logging.info('postbackData: ', backdata)

        except Exception as e:

            logging.error("Exception: ", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage
                                       (text=f'發生錯誤，請聯絡管理員!\n \
                                        信箱：{config.TEAM_EMAIL}'))

        else:

            if backtype == 'sendConfirm':
                result = searchByCode(backdata)
                sendContent(event, result)


def sendConfirm(event, result, typeButton):
    message = []
    try:
        message.append(TextSendMessage(f'以下是{result[1]}的申辦資格'))
        if re.match('.*尚未填寫申辦說明', result[6]) or len(result[6]) == 1:
            message.append(TextSendMessage
                           ('目前相關單位還沒填寫詳情，請直接點選查看更多至網頁查看更詳細資訊。'))
        else:
            message.append(TextSendMessage(f'{result[6]}'))

        message.append(TemplateSendMessage(
            alt_text='津貼條件',
            template=ConfirmTemplate(
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
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        logging.error("Exception: ", e)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤!'))


def sendQuickreply(event, listData, typeButton):
    actionsList = []

    match typeButton:
        case "selectLocation":
            text = '請問您的戶籍地是台灣哪區呢?'
        case "selectBigLocation":
            text = '請問您的戶籍地是哪個縣市呢?'
        case "selectCategory":
            text = '請問您今天想要查詢哪個類別的津貼呢?'

    for item in listData:
        actionsList.append(QuickReplyButton(action=MessageAction
                                            (label=item, text=item,
                                             data=f'action={typeButton}, \
                                             data={item}')))
    try:
        message = TextSendMessage(
            text=text,
            quick_reply=QuickReply(
              items=actionsList
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        logging.error("Exception: ", e)
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤!'))


def sendContent(event, result):
    message = []
    logging.info(result)
    if re.match('.*尚未填寫申辦說明', result[5]) or len(result[5]) == 1:
        message.append(TextSendMessage
                       (text='目前相關單位還沒填寫詳情，請直接點選查看更多至網頁查看更詳細資訊。'))
    else:
        message.append(TextSendMessage(text=result[5]))
    try:
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤!'))
        logging.error("Exception: ", e)


def sendList(event, category, location, result):
    message = []
    text = ""
    for index, list in enumerate(result):
        if index == len(result) - 1:
            text += list[0]+" "+list[1]
        else:
            text += list[0]+" "+list[1]+"\n"
    message.append(TextSendMessage(text=text))
    message.append(TextSendMessage(f'以上是中央政府及{location}的{category} 相關的津貼ID列表'))
    message.append(TextSendMessage('請在訊息視窗輸入津貼前面的數字(ID)查詢津貼的詳情'))

    try:
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(text='發生錯誤!'))
        logging.error("Exception: ", e)
