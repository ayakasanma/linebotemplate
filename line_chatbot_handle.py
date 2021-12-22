from line_chatbot_api import *
from access_sqlite_db import *
import random, os, json, sqlite3
import speech_recognition as sr # pip install SpeechRecognition
from urllib.parse import parse_qsl, parse_qs

user_weight=None
user_height=None
user_age=None

def transcribe(wav_path):
    '''
    Speech to Text by Google free API
    language: en-US, zh-TW
    '''
    
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        return r.recognize_google(audio, language="zh-TW")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return None


def function_handle_something(event, user_data):
    line_user_name = line_bot_api.get_profile(event.source.user_id).display_name
    line_user_id = event.source.user_id
    global user_weight
    global user_height
    global user_age
    user_weight = user_data[2] if user_data[2] else None
    user_height = user_data[3] if user_data[3] else None
    user_age = user_data[4] if user_data[4] else None
    if event.message.type=='text':
        print(event.message)
        recrive_text=event.message.text
        # print(recrive_text)
        if '服務' in recrive_text:
            # print(url_for('static', filename='images/brown_1024.jpg', _external=True))
            call_service(event, user_data)
        elif '索取備品' in recrive_text:
            ask_tower_or_something(event)
        elif '客房介紹' in recrive_text:
            messages=[]
            messages.append(ImageSendMessage(original_content_url='https://i.imgur.com/H8O5GVT.png', preview_image_url='https://i.imgur.com/JM2MHSi.png'))
            messages.append(TextSendMessage(text='這次入住的是中央飯店的經典客房，客房裝潢以溫暖的大地色系為基調，簡約時尚的設計風格，搭配大片落地玻璃窗，讓自然陽光灑入，住客能在舒適的房間內，遠眺樹海美景及飽覽中壢都會景觀。簡潔俐落的線條經過細節化處理，呈現客房空間設計的時尚氛圍及本真之美。'))
            messages.append(another_service_or_not)
            line_bot_api.reply_message(event.reply_token, messages)  
        elif '美食地圖' in recrive_text:
            call_food(event)
        elif '中式餐點小吃' in recrive_text:
            call_Chinese_food(event)
        elif '西式餐點小吃' in recrive_text:
            call_western_food(event)
        elif '生態導覽' in recrive_text:
            messages=[]
            messages.append(StickerSendMessage(package_id=446, sticker_id=2000))
            messages.append(TextSendMessage(text='中央飯店正努力撰寫程式碼中，請稍後再回來查看此功能~ 謝謝您~'))
            line_bot_api.reply_message(event.reply_token, messages)
        elif '設定體重' == recrive_text:
            update_user_action(line_user_id, 'set_weight')
            message = TextSendMessage(text='請輸入您的體重(公斤)')
            line_bot_api.reply_message(event.reply_token, message)
        elif '設定身高' == recrive_text:
            update_user_action(line_user_id, 'set_height')
            message = TextSendMessage(text='請輸入您的身高(公分)')
            line_bot_api.reply_message(event.reply_token, message)
        elif '設定年紀' == recrive_text:
            update_user_action(line_user_id, 'set_age')
            message = TextSendMessage(text='請輸入您的年紀(歲)')
            line_bot_api.reply_message(event.reply_token, message)
        elif '計算BMI' == recrive_text:
            message = TextSendMessage(text=f'BMI為{user_weight/((user_height/100)**2):.1f}')
            line_bot_api.reply_message(event.reply_token, message)
        elif '計算BMR' == recrive_text:
            message = TextSendMessage(text=f'BMR為{user_age*user_weight/((user_height/100)**2):.1f}')
            line_bot_api.reply_message(event.reply_token, message)
        elif read_user_action(line_user_id):
            user_action = read_user_action(line_user_id)
            if user_action == 'set_weight':
                if recrive_text.isnumeric():
                    update_user_weight(line_user_id, recrive_text)
                    update_user_action(line_user_id, '')
                    user_data = read_user_data(line_user_id, line_user_name)
                    user_weight = user_data[2] if user_data[2] else None
                    user_height = user_data[3] if user_data[3] else None
                    user_age = user_data[4] if user_data[4] else None
                    message = TextSendMessage(text='體重設定成功',
                                            quick_reply=QuickReply(items=[
                                                QuickReplyButton(action=MessageAction(label=f"體重{user_weight}公斤" if user_weight else "體重未設定", text="設定體重")),
                                                QuickReplyButton(action=MessageAction(label=f"身高{user_height}公分" if user_height else "身高未設定", text="設定身高")),
                                                QuickReplyButton(action=MessageAction(label=f"年紀{user_age}歲" if user_age else "年紀未設定", text="設定年紀"))
                                                ]))
                else:
                    message = TextSendMessage(text='請輸入數字')
                line_bot_api.reply_message(event.reply_token, message)
            elif user_action == 'set_height':
                if recrive_text.isnumeric():
                    update_user_height(line_user_id, recrive_text)
                    update_user_action(line_user_id, '')
                    user_data = read_user_data(line_user_id, line_user_name)
                    user_weight = user_data[2] if user_data[2] else None
                    user_height = user_data[3] if user_data[3] else None
                    user_age = user_data[4] if user_data[4] else None
                    message = TextSendMessage(text='身高設定成功',
                                            quick_reply=QuickReply(items=[
                                                QuickReplyButton(action=MessageAction(label=f"體重{user_weight}公斤" if user_weight else "體重未設定", text="設定體重")),
                                                QuickReplyButton(action=MessageAction(label=f"身高{user_height}公分" if user_height else "身高未設定", text="設定身高")),
                                                QuickReplyButton(action=MessageAction(label=f"年紀{user_age}歲" if user_age else "年紀未設定", text="設定年紀"))
                                                ]))
                else:
                    message = TextSendMessage(text='請輸入數字')
                line_bot_api.reply_message(event.reply_token, message)
            elif user_action == 'set_age':
                if recrive_text.isnumeric():
                    update_user_age(line_user_id, recrive_text)
                    update_user_action(line_user_id, '')
                    user_data = read_user_data(line_user_id, line_user_name)
                    user_weight = user_data[2] if user_data[2] else None
                    user_height = user_data[3] if user_data[3] else None
                    user_age = user_data[4] if user_data[4] else None
                    message = TextSendMessage(text='年紀設定成功',
                                            quick_reply=QuickReply(items=[
                                                QuickReplyButton(action=MessageAction(label=f"體重{user_weight}公斤" if user_weight else "體重未設定", text="設定體重")),
                                                QuickReplyButton(action=MessageAction(label=f"身高{user_height}公分" if user_height else "身高未設定", text="設定身高")),
                                                QuickReplyButton(action=MessageAction(label=f"年紀{user_age}歲" if user_age else "年紀未設定", text="設定年紀"))
                                                ]))
                else:
                    message = TextSendMessage(text='請輸入數字')
                line_bot_api.reply_message(event.reply_token, message)
        else:
            messages=[]
            messages.append(StickerSendMessage(package_id=789, sticker_id=10882))
            messages.append(TextSendMessage(text='抱歉我沒聽懂~ 可以用其他方式再說一次嗎?'))
            line_bot_api.reply_message(event.reply_token, messages)
    elif event.message.type=='sticker':
        receive_sticker_id=event.message.sticker_id
        receive_package_id=event.message.package_id
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=receive_package_id, sticker_id=receive_sticker_id))
    elif event.message.type=='image':
        message_content = line_bot_api.get_message_content(event.message.id)
        with open('temp_image.png', 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
    elif event.message.type=='audio':
        filename_wav='temp_audio.wav'
        filename_mp3='temp_audio.mp3'
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(filename_mp3, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        os.system(f'ffmpeg -y -i {filename_mp3} {filename_wav} -loglevel quiet')
        text = transcribe(filename_wav)
        # print('Transcribe:', text)
        if '服務' in text:
            # print(url_for('static', filename='images/brown_1024.jpg', _external=True))
            call_service(event)
def call_service(event, data):
    line_user_name = line_bot_api.get_profile(event.source.user_id).display_name
    line_user_id = event.source.user_id
    global user_weight
    global user_height
    global user_age
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
            title='請問需要什麼服務呢?',
            text='請在下方點選您需要的服務項目',
            actions=[
                MessageAction(
                    label='索取備品(毛巾、礦泉水...等)',
                    text='索取備品'
                ),
                MessageAction(
                    label='客房介紹',
                    text='客房介紹'
                ),
                MessageAction(
                    label='計算BMI',
                    text='計算BMI'),
                MessageAction(
                    label='計算BMR',
                    text='計算BMR'),
            ]
        ),
        quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label=f"體重{user_weight}公斤" if user_weight else "體重未設定", text="設定體重")),
                QuickReplyButton(action=MessageAction(label=f"身高{user_height}公分" if user_height else "身高未設定", text="設定身高")),
                QuickReplyButton(action=MessageAction(label=f"年紀{user_age}歲" if user_age else "年紀未設定", text="設定年紀"))
                ])
    )
    line_bot_api.reply_message(event.reply_token, message)
    

def ask_tower_or_something(event):
    message = TemplateSendMessage(
        alt_text='索取備品',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='毛巾類',
                    text='請問想索取哪一種備品',
                    actions=[
                        PostbackAction(
                            label='毛巾',
                            display_text='想索取毛巾',
                            data='action=索取備品&item=毛巾'
                        ),
                        PostbackAction(
                            label='浴巾',
                            display_text='想索取浴巾',
                            data='action=索取備品&item=浴巾'
                        ),
                        PostbackAction(
                            label='方巾',
                            display_text='想索取方巾',
                            data='action=索取備品&item=方巾'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='清潔用品',
                    text='請問想索取哪一種請潔用品',
                    actions=[
                        PostbackAction(
                            label='沐浴乳',
                            display_text='想索取沐浴乳',
                            data='action=索取備品&item=沐浴乳'
                        ),
                        PostbackAction(
                            label='洗髮精',
                            display_text='想索取洗髮精',
                            data='action=索取備品&item=洗髮精'
                        ),
                        PostbackAction(
                            label='乳液',
                            display_text='想索取乳液',
                            data='action=索取備品&item=乳液'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/rfgMcFM.jpg',
                    title='其他備品',
                    text='請問想索取哪一種備品',
                    actions=[
                        PostbackAction(
                            label='礦泉水',
                            display_text='想索取礦泉水',
                            data='action=索取備品&item=礦泉水'
                        ),
                        PostbackAction(
                            label='3合1沖泡咖啡包',
                            display_text='想索取3合1沖泡咖啡包',
                            data='action=索取備品&item=3合1沖泡咖啡包'
                        ),
                        PostbackAction(
                            label='紅茶茶包',
                            display_text='想索取紅茶茶包',
                            data='action=索取備品&item=紅茶茶包'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

another_service_or_not = TemplateSendMessage(
    alt_text='Confirm template',
    template=ConfirmTemplate(
        text='請問還需要其他服務嗎?',
        actions=[
            PostbackAction(
                label='還需要服務',
                display_text='還需要服務',
                data='action=還需要服務'
            ),
            PostbackAction(
                label='暫時先不用',
                display_text='暫時先不用',
                data='action=暫時先不用其他服務'
            )
        ]
    )
)


foodlist=[]
foodlist.append(('C', '廚窗 Kitchen Bliss', '324桃園市平鎮區中央路157號', '+886987078449', 24.9648154,121.1908407))
foodlist.append(('C', '阿米玲食堂', '320桃園市中壢區中央路212號', '+88634204995', 24.9644749,121.1907892))
foodlist.append(('W', '迷路義麵屋', '320桃園市平鎮區中央路151號', '+88634202713', 24.9647471,121.1907073))
foodlist.append(('W', '大中央厚切牛排', '320桃園市中壢區中央路153號', '+88634201415', 24.9647471,121.1907073))

foodstickerlist=[]
foodstickerlist.append((446, 1996))
foodstickerlist.append((446, 1997))
foodstickerlist.append((446, 1998))
foodstickerlist.append((789, 10865))
foodstickerlist.append((789, 10866))
foodstickerlist.append((789, 10863))

def call_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='想吃什麼，可以幫您推薦喔',
            text='可以選擇你想吃的餐飲類型，或是隨機由小編推薦',
            actions=[
                MessageAction(
                    label='中式餐點小吃',
                    text='中式餐點小吃'
                ),
                MessageAction(
                    label='西式餐點小吃',
                    text='西式餐點小吃'
                ),
                PostbackAction(
                    label='隨機推薦餐點',
                    display_text='隨機推薦餐點小吃',
                    data=f'action=food&item={json.dumps(foodlist[random.randint(0,len(foodlist)-1)])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def call_Chinese_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='這裡推薦幾間不錯的中式餐點',
            text='可以參考一下喔',
            actions=[
                PostbackAction(
                    label=foodlist[0][1],
                    display_text=foodlist[0][1],
                    data=f'action=food&item={json.dumps(foodlist[0])}'
                ),
                PostbackAction(
                    label=foodlist[1][1],
                    display_text=foodlist[1][1],
                    data=f'action=food&item={json.dumps(foodlist[1])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def call_western_food(event):
    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            # thumbnail_image_url=url_for('static', filename='images/brown_1024.jpg', _external=True),
            thumbnail_image_url='https://i.imgur.com/mfUIthQ.png',
            title='這裡推薦幾間不錯的西式餐點',
            text='可以參考一下喔',
            actions=[
                PostbackAction(
                    label=foodlist[2][1],
                    display_text=foodlist[2][1],
                    data=f'action=food&item={json.dumps(foodlist[2])}'
                ),
                PostbackAction(
                    label=foodlist[3][1],
                    display_text=foodlist[3][1],
                    data=f'action=food&item={json.dumps(foodlist[3])}'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

def show_food(event, food):
    foodsticker = foodstickerlist[random.randint(0,len(foodstickerlist)-1)]
    messages=[]
    messages.append(StickerSendMessage(package_id=foodsticker[0], sticker_id=foodsticker[1]))
    messages.append(TextSendMessage(text=f'為您推薦：{food[1]}，地址：{food[2]}，電話：{food[3]}'))
    # messages.append(LocationSendMessage())
    messages.append(LocationSendMessage(title=food[1], address=food[2], latitude=food[4], longitude=food[5]))
    line_bot_api.reply_message(event.reply_token, messages)