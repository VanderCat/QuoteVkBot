from PIL import ImageFont, Image, ImageDraw, ImageFilter
import textwrap
import urllib.request as rq
"""Make QOGP"""
def mkmask(size,color=255):
    img = Image.new("L", (size*5,size*5))
    d = ImageDraw.Draw(img)
    d.ellipse((0,0,size*5,size*5),color)
    return img.resize((size,size), resample=Image.LANCZOS)
def mkshadow(img, xy, fill=60,blur=2):
    shadow = Image.new("L", img.size)
    ds = ImageDraw.Draw(shadow)
    ds.rectangle(xy,fill=fill)
    img.paste(Image.new("RGB", img.size, (0,0,0)), mask=shadow.filter(ImageFilter.GaussianBlur(blur)))
def mkshadowround(img, xy, fill=60,blur=7):
    shadow = Image.new("L", img.size)
    ds = ImageDraw.Draw(shadow)
    ds.ellipse(xy,fill=fill)
    img.paste(Image.new("RGB", img.size, (0,0,0)), mask=shadow.filter(ImageFilter.GaussianBlur(blur)))
def text_wrap(text,font,writing,max_width):
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        w = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)[0]
        if w > max_width: # too wide
            # take it back out, put it on the next line, then measure again
            lines.append([lines[-1].pop()])
            w = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)[0]
    return '\n'.join([' '.join(line) for line in lines]) #Function by https://stackoverflow.com/users/13639308/chris-jones
def mk(object, alpha=False):
    #Setup fonts
    FontHeader = ImageFont.truetype("font/Roboto/Medium.ttf", 20*object.settings.size) #"font/Roboto/Medium.ttf"
    FontMessage = ImageFont.truetype("font/Roboto/Regular.ttf", 14*object.settings.size) #"font/Roboto/Regular.ttf"
    FontAuthor = ImageFont.truetype("font/Roboto/Regular.ttf", 10*object.settings.size) #"font/Roboto/Regular.ttf"

    tmp = Image.new("1", (512*object.settings.size,512*object.settings.size), 0)
    dtmp = ImageDraw.Draw(tmp)
    #Setup messages
    messages = ""
    for msg in object.textbody.maintext:
        messages += '"'
        i = 0
        for line in msg.split("\n"):
            if i == len(msg.split("\n"))-1:
                line += "\"\n"
            messages += text_wrap(line,FontMessage,dtmp,(object.settings.width-152-object.settings.margin[1]-object.settings.margin[3])*object.settings.size) + "\n" #textwrap.fill(msg, 40,replace_whitespace=False)
            i+=1
    
    #prepare image
    color = ()
    mode = ""
    if alpha == True:
        color = (229,229,229,0)
        mode = "RGBA"
    else:
        color = (229,229,229)
        mode = "RGB"
    img = Image.new(mode, (object.settings.width*object.settings.size, object.settings.minheight*object.settings.size + object.settings.margin[0]*object.settings.size + object.settings.margin[2]*object.settings.size), color)
    d = ImageDraw.Draw(img) 
    txth = d.multiline_textsize(messages,FontMessage)[1]
    print(txth)
    #prepare image if higher
    if txth > 44*object.settings.size:
        img = Image.new(mode, (object.settings.width*object.settings.size,txth + object.settings.margin[0]*object.settings.size + object.settings.margin[2]*object.settings.size+84*object.settings.size), color)
        d = ImageDraw.Draw(img)
    
    #shapes
    mkshadow(img,(object.settings.margin[3]*object.settings.size+64*object.settings.size, object.settings.margin[0]*object.settings.size+30*object.settings.size+2*object.settings.size, object.settings.width*object.settings.size-object.settings.margin[1]*object.settings.size-7*object.settings.size,img.size[1]-object.settings.margin[2]*object.settings.size+2*object.settings.size),blur=2*object.settings.size)
    d.rectangle( (object.settings.margin[3]*object.settings.size+64*object.settings.size, object.settings.margin[0]*object.settings.size+30*object.settings.size, object.settings.width*object.settings.size-object.settings.margin[1]*object.settings.size-7*object.settings.size,img.size[1]-object.settings.margin[2]*object.settings.size),fill=(230,230,230), outline=(214,214,214),width=1*object.settings.size)

    mkshadow(img, (object.settings.margin[3]*object.settings.size+64*object.settings.size,object.settings.margin[0]*object.settings.size+6*object.settings.size,object.settings.width*object.settings.size-object.settings.margin[1]*object.settings.size,img.size[1]-object.settings.margin[2]*object.settings.size-30*object.settings.size+6*object.settings.size),blur=5*object.settings.size)
    d.rectangle((object.settings.margin[3]*object.settings.size+64*object.settings.size,object.settings.margin[0]*object.settings.size,object.settings.width*object.settings.size-object.settings.margin[1]*object.settings.size,img.size[1]-object.settings.margin[2]*object.settings.size-30*object.settings.size),fill=(255,255,255), outline=(246,246,246),width=1*object.settings.size)

    mkshadowround(img, (object.settings.margin[0]*object.settings.size,object.settings.margin[3]*object.settings.size,object.settings.margin[0]*object.settings.size+128*object.settings.size,object.settings.margin[3]*object.settings.size+128*object.settings.size),blur=7*object.settings.size)
    img.paste(Image.open(rq.urlopen(object.image)).convert('RGB').resize((128*object.settings.size,128*object.settings.size)), (object.settings.margin[0]*object.settings.size,object.settings.margin[3]*object.settings.size),mkmask(128*object.settings.size))

    #55+txth.filter(ImageFilter.GaussianBlur(7)
    #header
    d.text((object.settings.margin[3]*object.settings.size+140*object.settings.size,object.settings.margin[0]*object.settings.size+33*object.settings.size), "Цитаты великих людей:", font=FontHeader, anchor="ls", fill=(0, 0, 0))

    #messages 
    d.multiline_text((object.settings.margin[3]*object.settings.size+140*object.settings.size,object.settings.margin[0]*object.settings.size+44*object.settings.size), messages, font=FontMessage, fill=(0, 0, 0))

    #from
    d.text((object.settings.width*object.settings.size-object.settings.margin[3]*object.settings.size-12*object.settings.size,img.size[1]-object.settings.margin[2]*object.settings.size-10*object.settings.size), "ОТ " + object.textbody.name.upper() + ", " + object.textbody.date, font=FontAuthor, anchor="rs", fill=(0, 0, 0))
    return img