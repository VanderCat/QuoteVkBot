from PIL import ImageFont, Image, ImageDraw
import textwrap
import urllib.request as rq
"""Make QOFP"""
def mkmask():
    img = Image.new("L", (150*5,150*5))
    d = ImageDraw.Draw(img)
    d.ellipse((0,0,150*5,150*5),255)
    return img.resize((150,150), resample=Image.LANCZOS)
def mk(object):
    fnt = ImageFont.truetype("font/Inter/Inter-VariableFont_slnt,wght.ttf", 24)
    fntmsg = ImageFont.truetype("font/Inter/Inter-VariableFont_slnt,wght.ttf", 18)
    messages = ""
    if not isinstance(object.textbody.maintext, str):
        for msg in object.textbody.maintext:
            messages += '"' + textwrap.fill(msg, 40,replace_whitespace=False) + "\"\n"
            print(msg)
    else:
        messages = '"' + object.textbody.maintext +'"'
    print(messages)
    img = Image.new("RGB", object.wh, (51,51,51))
    d = ImageDraw.Draw(img)
    txth = d.multiline_textsize(messages,fntmsg)[1]
    if txth > 150:
        img = Image.new("RGB", (object.wh[0],txth+110), (51,51,51))
        d = ImageDraw.Draw(img)
    d.text((165,35), "Цитаты великих людей:", font=fnt, anchor="ls", fill=(255, 255, 255))
    d.multiline_text((200,55), messages, font=fntmsg, fill=(255, 255, 255))
    d.text((620,img.size[1]-20), "© " + object.textbody.name + ", " + object.textbody.date, font=fntmsg, anchor="rs", fill=(255, 255, 255))
    img.paste(Image.open(rq.urlopen(object.imageurl)).convert('RGB').resize((150,150)), (25,55),mkmask())
    return img