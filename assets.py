from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
atlas=Image.new('L',(1024,2048));d=ImageDraw.Draw(atlas);header=[];y=2
labels=[('TITLE','ftpd-sb',58),('SUB','Wireless file transfer',24),('FTP','FTP',96),('CONNECTION','CONNECTION',19),('LOGIN','Anonymous FTP',24),('OFF','Stopped',26),('ON','Ready to connect',26),('CONNECTED','Connected',26),('TRANSFER','Transferring',26),('ERROR','Could not start server',26),('WAIT','Starting...',26),('START','A  Start',24),('STOP','A  Stop',24),('EXIT','B  Back',24),('CREDIT','Created W/ AI (@RavensClawX)',15)]
for name,label,size in labels:
 face=ImageFont.truetype(font,size);b=d.textbbox((0,0),label,font=face);w,h=b[2]-b[0],b[3]-b[1]
 d.text((2-b[0],y-b[1]),label,font=face,fill=255);header.append(f'const ivec4 TEXT_{name}=ivec4(2,{y},{w},{h});');y+=h+9
face=ImageFont.truetype(mono,48);gy=y+8
for i,char in enumerate('0123456789.:'):
 d.text((i*40,gy),char,font=face,fill=255)
header.append(f'const int DIGIT_Y={gy};')
assert gy+64<2048
(root/'assets/text.bin').write_bytes(atlas.tobytes());(root/'shaders/text.glsl').write_text('\n'.join(header)+'\n')
im=Image.new('RGBA',(256,256),(250,251,253,255));p=ImageDraw.Draw(im)
for at in range(0,256,32):
 p.line((at,0,at,255),fill=(225,230,236),width=1);p.line((0,at,255,at),fill=(225,230,236),width=1)
blue=(30,109,225)
p.line((50,94,197,94),fill=blue,width=10);p.polygon([(177,72),(207,94),(177,116)],fill=blue)
p.line((59,160,206,160),fill=blue,width=10);p.polygon([(79,138),(49,160),(79,182)],fill=blue)
im.save(root/'assets/icon.png')
