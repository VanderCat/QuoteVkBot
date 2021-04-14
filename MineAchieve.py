#32 + txtw + 6
#bottom offset 17

from PIL import ImageFont, Image, ImageDraw, ImageFilter
import os
import random

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
    #Setup font
    Font = ImageFont.truetype("font/mineedit.ttf", 8) 
    #Setup message
    print(object.textbody.maintext[0])
    message = object.textbody.maintext[0].split("\n")
    
    print(message)

    img = Image.new("1", (1, 1), 1)
    d = ImageDraw.Draw(img) 
    txtmeasure1 = d.multiline_textsize(message[0],Font)
    txtmeasure2 = d.multiline_textsize(message[1],Font)
    if txtmeasure1[0]+32>txtmeasure2[0]:
        class width:
            front = txtmeasure1[0]
            back =  txtmeasure1[0] +32 +6
            backend = -4
            image = txtmeasure1[0] +32 +6
    else:
        class width:
            front = txtmeasure2[0] -29
            back = txtmeasure2[0]
            backend = +5
            image = txtmeasure2[0] +9
    print(width)

    texture_atlas = Image.open("Images/index.png")
    class texture:
        class front:
            start = texture_atlas.crop((0,3,4,23))
            loop = texture_atlas.crop((4,3,5,23))
            end = texture_atlas.crop((196,3,200,23))
        class back:
            start = texture_atlas.crop((0,55,4,75))
            loop = texture_atlas.crop((4,55,5,75))
            end = texture_atlas.crop((196,55,200,75))
        blob = texture_atlas.crop((1,155,25,179))

    #prepare image
    color = ()
    if alpha == True:
        color = (0,0,0,0)
    else:
        color = (255,255,255,255)
    img = Image.new("RGBA", (width.image, 37), color) #(32 + txtmeasure[0] + 6)
    d = ImageDraw.Draw(img) 

    temp = Image.new("RGBA", img.size, (0,0,0,0))
    temp.paste(texture.back.start, (0,17))
    temp.paste(texture.back.loop.resize((width.back+1,20),0), (4,17))
    temp.paste(texture.back.end, (width.back+width.backend,17))
    img.alpha_composite(temp)

    temp = Image.new("RGBA", img.size, (0,0,0,0))
    temp.paste(texture.front.start, (0,2))
    temp.paste(texture.front.loop.resize((32+width.front+6,20),0), (4,2))
    temp.paste(texture.front.end, (32+width.front+2,2))
    img.alpha_composite(temp)

    temp = Image.new("RGBA", img.size, (0,0,0,0))
    temp.paste(texture.blob, (4,0))
    img.alpha_composite(temp)
    
    rand = os.listdir(path="Images/items/")
    rand = rand[random.randint(0,len(rand)-1)]
    if len(message) == 2:
        message.append(random)
    else:
        message[2] = message[2]+".png"
    temp = Image.new("RGBA", img.size, (0,0,0,0))
    try:
        temp.paste(Image.open("Images/items/"+message[2]), (8,4))
    except:
        temp.paste(Image.open("Images/items/"+rand), (8,4))
    img.alpha_composite(temp)
    #7shad 6txt

    d.text((33,9),message[0],fill=(0,0,0),font=Font)
    d.text((32,8),message[0],fill=(255,255,255),font=Font)
    d.text((5,25),message[1],fill=(110,235,110),font=Font)

    return img.resize((img.size[0]*object.settings.size,img.size[1]*object.settings.size),0)


if __name__ == "__main__":
    class obj:
        class textbody:
            maintext = ["цвл майsdasdasн\nверхний "]
        class settings:
            size = 8
            width = 512
            minheight = 128
            margin = [40,40,40,40] # [top,right,bottom,left]

    mk(obj).show()#.save("test.png")