import vk_api
import QOGP2
import MineAchieve
from datetime import datetime, timedelta
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests.exceptions

with open("token.vk", 'r') as f:
    token = f.readline()
vk_session = vk_api.VkApi(token=token)

vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, wait=25, group_id="189733255")
vku = vk_api.VkUpload(vk_session)
while True:
    try:
        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.obj
                print(text)
                if text["message"]["text"].lower().split(" ")[0] == 'цвл' and (("reply_message" in text["message"] and text["message"] != "" ) or len(text["message"]["fwd_messages"]) != 0):
                    usr = {}
                    tempdate = 0
                    if ("reply_message" in text["message"]):
                        tempdate = text['message']['date']
                        print("Temp data init")
                        try:
                            usr = vk.users.get(user_ids=[text["message"]["reply_message"]["from_id"]],fields=["photo_200"])
                        except:
                            usr = vk.groups.getById(group_id=-text["message"]["reply_message"]["from_id"],fields=["photo_200"])
                    else:
                        tempdate = text['message']['date']
                        print("Temp data init")
                        try:
                            usr = vk.users.get(user_ids=[text["message"]["fwd_messages"][0]["from_id"]],fields=["photo_200"])
                        except:
                            usr = vk.groups.getById(group_id=-text["message"]["fwd_messages"][0]["from_id"],fields=["photo_200"])
                    print("Got: " + str(usr))
        
                    class QOFPobj:
                        wh = (640,260)
                        image = usr[0]['photo_200']
                        class textbody:
                            maintext = []
                            lastid = ""
                            if "reply_message" in text["message"]:
                                lastid  = text['message']["reply_message"]["from_id"]
                                maintext += [text['message']['reply_message']['text']]
                            else:
                                lastid = text['message']['fwd_messages'][0]["from_id"]
                                for msg in text['message']['fwd_messages']:
                                    if msg["from_id"] == lastid:
                                        maintext += [msg["text"]]
                            date = str((datetime.utcfromtimestamp(tempdate) + timedelta(hours=3)).strftime('%H:%M:%S %m.%d.%Y'))
                            if "first_name" in usr[0]:
                                name = usr[0]['first_name'] + " " + usr[0]['last_name']
                            else:
                                name =usr[0]['name']
                        class settings:
                            size = 2
                            width = 512
                            minheight = 128
                            margin = [40,40,40,40] # [top,right,bottom,left]
                    print("Object created")
                    attachment = {'mydev':"temp"}
                    print(text["message"]["text"].lower().split("\n")[0].split(" "))
                    if len(text["message"]["text"].lower().split("\n")[0].split(" "))>=2:
                        if text["message"]["text"].lower().split("\n")[0].split(" ")[1] == "док":
                            QOGP2.mk(QOFPobj,True).save('img.png')
                            print("IMG Saved")
                            attachment = vku.document("img.png", group_id="189733255", message_peer_id=text['message']['peer_id'])
                            print("Document Uploaded")
                            vk.messages.send(peer_id=text['message']['peer_id'],random_id=random.randint(0,999),attachment='{}{}_{}'.format(attachment['type'],attachment['doc']['owner_id'], attachment['doc']['id']))
                        elif text["message"]["text"].lower().split("\n")[0].split(" ")[1] == "майн":
                            if len(QOFPobj.textbody.maintext[0].split("\n")) >= 2:
                                if text["message"]["text"].lower().split("\n")[0].split(" ")[2] == "док":
                                    MineAchieve.mk(QOFPobj,True).save('img.png')
                                    print("IMG Saved")
                                    attachment = vku.document("img.png", group_id="189733255", message_peer_id=text['message']['peer_id'])
                                    print("Document Uploaded")
                                    vk.messages.send(peer_id=text['message']['peer_id'],random_id=random.randint(0,999),attachment='{}{}_{}'.format(attachment['type'],attachment['doc']['owner_id'], attachment['doc']['id']))
                                else:
                                    MineAchieve.mk(QOFPobj).save('img.png')
                                    print("IMG Saved")
                                    attachment = vku.photo_messages("img.png", peer_id=text["message"]["peer_id"])
                                    print("Photo Uploaded")
                                    vk.messages.send(peer_id=text['message']['peer_id'],random_id=random.randint(0,999),attachment='photo{}_{}'.format(attachment[0]['owner_id'], attachment[0]['id']))
                            else:
                                vk.messages.send(peer_id=text['message']['peer_id'],random_id=random.randint(0,999),message="СКОЛЬКО ТЕБЕ ПОВТОРЯТЬ МОЖНО, 2 СТРОКИ НАДО >:C")
                    else:
                        QOGP2.mk(QOFPobj).save('img.png')
                        print("IMG Saved")
                        attachment = vku.photo_messages("img.png", peer_id=text["message"]["peer_id"])
                        print("Photo Uploaded")
                        vk.messages.send(peer_id=text['message']['peer_id'],random_id=random.randint(0,999),attachment='photo{}_{}'.format(attachment[0]['owner_id'], attachment[0]['id']))
                    print(attachment)
                    
    except requests.exceptions.ReadTimeout:
        pass
