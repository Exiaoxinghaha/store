# -*-coding:utf-8-*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random

# 生成随机颜色
def random_color(s=0,e=255):
    return (random.randint(s,e),random.randint(s,e),random.randint(s,e))

# 生成随机验证码
def verification_code(length=4):
    num_list = [str(i) for i in range(0,10)]
    str_list = [chr(i) for i in range(65,91)]
    str_list += [chr(i) for i in range(97,123)]
    char_list = num_list+str_list
    code_list = random.sample(char_list,length)
    verify_code =''.join(code_list)
    return verify_code

# 生成验证码图片
def verification_pic(width=80,height=25):
    image = Image.new(mode="RGB",size=(width,height),color=(255,255,255))
    draw = ImageDraw.Draw(image,mode='RGB',)
    font = ImageFont.truetype('static/bootstrap/fonts/Candarai.ttf',28)
    for x in range(width):
        for y in range(height):
            draw.point([x,y],fill=random_color(150,230))
    verify_code = verification_code(4)
    for i in verify_code:
        color = random_color(32,127)
        if verify_code.index(i)==0:
            draw.text([6,0],i,color,font=font)
        else:
            draw.text([verify_code.index(i)*20,0],i,color,font=font)
    # 模糊滤镜
    image = image.filter(ImageFilter.DETAIL)
    return image,verify_code
