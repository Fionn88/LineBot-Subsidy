from linebot.models import (
    TextSendMessage, TemplateSendMessage, QuickReplyButton, ConfirmTemplate, 
    PostbackTemplateAction,URITemplateAction,QuickReply,MessageAction
)
import re
from urls import line_bot_api



def sendConfirm(event,result,typeButton):
    message = []
    try:
        message.append(TextSendMessage(f'以下是{result[1]}的申辦資格'))
        
        if re.match('.*尚未填寫申辦說明|.*無', result[6]):
            message.append(TextSendMessage('目前相關單位還沒填寫詳情，請直接點選查看更多至網頁查看更詳細資訊。'))
        else:
            message.append(TextSendMessage(f'{result[6]}'))
        
        message.append(TemplateSendMessage(
            alt_text = '津貼條件',
            template = ConfirmTemplate(
                text='您還可以看看補助內容或查看更多：',
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
    elif typeButton == "selectLocation" or typeButton == "selectBigLocation":
        text = '請問您的戶籍地是台灣哪區呢?'
    elif typeButton == "selectLocation":
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
    if re.match('.*尚未填寫申辦說明|.*無', result[5]):
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