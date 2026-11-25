#!/usr/bin/env python3
import os, struct, zlib

W=H=1024
P=(246,243,235); K=(25,27,30); R=(172,39,44); G=(90,94,91); B=(35,69,102); C=(255,253,247)
# Each glyph is seven rows, left pixel first; all marks are authored here.
raw={
'A':('01110','10001','10001','11111','10001','10001','10001'),'B':('11110','10001','10001','11110','10001','10001','11110'),
'C':('01111','10000','10000','10000','10000','10000','01111'),'D':('11110','10001','10001','10001','10001','10001','11110'),
'E':('11111','10000','10000','11110','10000','10000','11111'),'F':('11111','10000','10000','11110','10000','10000','10000'),
'G':('01111','10000','10000','10111','10001','10001','01111'),'H':('10001','10001','10001','11111','10001','10001','10001'),
'I':('11111','00100','00100','00100','00100','00100','11111'),'J':('00111','00010','00010','00010','10010','10010','01100'),
'K':('10001','10010','10100','11000','10100','10010','10001'),'L':('10000','10000','10000','10000','10000','10000','11111'),
'M':('10001','11011','10101','10101','10001','10001','10001'),'N':('10001','11001','10101','10011','10001','10001','10001'),
'O':('01110','10001','10001','10001','10001','10001','01110'),'P':('11110','10001','10001','11110','10000','10000','10000'),
'Q':('01110','10001','10001','10001','10101','10010','01101'),'R':('11110','10001','10001','11110','10100','10010','10001'),
'S':('01111','10000','10000','01110','00001','00001','11110'),'T':('11111','00100','00100','00100','00100','00100','00100'),
'U':('10001','10001','10001','10001','10001','10001','01110'),'V':('10001','10001','10001','10001','10001','01010','00100'),
'W':('10001','10001','10001','10101','10101','11011','10001'),'X':('10001','10001','01010','00100','01010','10001','10001'),
'Y':('10001','10001','01010','00100','00100','00100','00100'),'Z':('11111','00001','00010','00100','01000','10000','11111'),
'0':('01110','10001','10011','10101','11001','10001','01110'),'1':('00100','01100','00100','00100','00100','00100','01110'),
'2':('01110','10001','00001','00110','01000','10000','11111'),'3':('11110','00001','00001','01110','00001','00001','11110'),
'4':('00010','00110','01010','10010','11111','00010','00010'),'5':('11111','10000','11110','00001','00001','10001','01110'),
'6':('00110','01000','10000','11110','10001','10001','01110'),'7':('11111','00001','00010','00100','01000','01000','01000'),
'8':('01110','10001','10001','01110','10001','10001','01110'),'9':('01110','10001','10001','01111','00001','00010','01100'),
' ':('00000',)*7,'-':('00000','00000','00000','11111','00000','00000','00000'),
'.':('00000','00000','00000','00000','00000','00110','00110'),',':('00000','00000','00000','00000','00110','00110','00100'),
':':('00000','00110','00110','00000','00110','00110','00000'),"'":('00100','00100','01000','00000','00000','00000','00000'),
'/':('00001','00010','00010','00100','01000','01000','10000'),'+':('00000','00100','00100','11111','00100','00100','00000'),
'%':('11001','11010','00010','00100','01000','01011','10011'),'?':('01110','10001','00001','00110','00100','00000','00100'),
'&':('01100','10010','10100','01000','10101','10010','01101')}
F={c:tuple(sum((ch=='1')<<(4-i) for i,ch in enumerate(row)) for row in rows) for c,rows in raw.items()}
S=[
('HOUTHI STRIKE','25 NOV 2026','REUTERS','HOUTHIS HIT SAUDI PIF TOWER IN RIYADH; 11 INJURED'),
('DRONES DOWNED','25 NOV 2026','ANADOLU','COALITION INTERCEPTS 4 DRONES OVER RAS TANURA'),
('HORMUZ MINES','25 NOV 2026','ANADOLU','IRGC SAYS 2 TANKERS HIT MINES, FIRE IN STRAIT OF HORMUZ'),
('PYONGYANG ROW','25 NOV 2026','REUTERS','NORTH KOREA EXPELS SWISS DIPLOMATIC CHIEF'),
('UKRAINE TALKS','25 NOV 2026','FT','US SHELVES RUSSIA BUSINESS-DEAL PLAN TO END WAR'),
('IRAN WAR','25 NOV 2026','J POST','TRUMP SAYS IRAN WAR FUNDING LASTS TO JANUARY'),
('JEDDAH THREAT','25 NOV 2026','REUTERS','HOUTHIS THREATEN JEDDAH AND SAUDI RED SEA PORTS'),
('PUTIN VOW','25 NOV 2026','ANADOLU','PUTIN SAYS ANSWER TO REFINERY ATTACKS IS INEVITABLE'),
('US ALERT','25 NOV 2026','HT','FRESH US SECURITY ALERT FOR AMERICANS IN MIDEAST'),
('NEW TARIFFS','24 NOV 2026','WSJ','US PREPARES TARIFFS ON CHINA, EU AND 14 PARTNERS'),
('HUAWEI VERDICT','25 NOV 2026','10THINGS','HUAWEI CONVICTED IN LANDMARK US CRIMINAL TRIAL'),
('CARACAS DEBT','24 NOV 2026','FT','VENEZUELA UNVEILS $237.5BN PUBLIC DEBT'),
('SHANGHAI PROBE','25 NOV 2026','10THINGS','SHANGHAI PARTY CHIEF FACES CORRUPTION PROBE'),
('ROHINGYA RETURN','25 NOV 2026','10THINGS','MALAYSIA TO RETURN THOUSANDS OF REFUGEES TO MYANMAR'),
('CUBA BLOCKADE','25 NOV 2026','10THINGS','WHO CHIEF CALLS FOR END TO US FUEL BLOCKADE ON CUBA'),
('PARIS TRIAL','25 NOV 2026','10THINGS','SARKOZY AND BRUNI FACE WITNESS TAMPERING TRIAL'),
('SPACEFLIGHT','25 NOV 2026','10THINGS','CHINA LAUNCHES FIRST JOINT INTERNATIONAL SPACEFLIGHT'),
('LANDMINES','25 NOV 2026','10THINGS','GLOBAL LANDMINE CASUALTIES REACH A FIVE-YEAR HIGH'),
('TAIZ OFFENSIVE','25 NOV 2026','ANADOLU','YEMENI TROOPS KILL 27 HOUTHIS IN SOUTHWEST TAIZ'),
('TURKEY PARDON','25 NOV 2026','NEWS9','TRUMP PARDONS THANKSGIVING TURKEYS AT WHITE HOUSE'),
('LIBYA TOLL','25 NOV 2026','WTOP','2 LIBYAN OFFICERS KILLED IN ATTACK ON RUSSIAN SHIP')]

def main():
    img=bytearray(bytes(P)*(W*H))
    def box(x,y,w,h,col):
        px=bytes(col)
        for yy in range(max(0,y),min(H,y+h)):
            a=(yy*W+max(0,x))*3;b=(yy*W+min(W,x+w))*3
            if b>a: img[a:b]=px*((b-a)//3)
    def txt(x,y,s,col=K,scale=1,limit=999):
        s=s.upper()[:limit]
        for ch in s:
            g=F.get(ch,F['?'])
            for ry,row in enumerate(g):
                for rx in range(5):
                    if row&(16>>rx): box(x+rx*scale,y+ry*scale,scale,scale,col)
            x+=6*scale
        return x
    def wrap(s,n):
        out=[]; line=''
        for word in s.split():
            q=(line+' '+word).strip()
            if len(q)>n and line: out.append(line);line=word
            else: line=q
        if line: out.append(line)
        return out
    box(0,0,W,H,P); box(0,0,W,9,K);box(0,9,W,3,R)
    txt(30,27,'THE WIRE',K,6)
    txt(575,48,'WEDNESDAY 25 NOVEMBER 2026',R,2)
    box(30,91,964,2,K)
    txt(30,105,'WORLD NEWS - 21 DATE-CHECKED DISPATCHES',K,2)
    txt(30,131,'EDITION 25 NOV 2026  ·  EVERY DISPATCH SHOWS REPORTING DATE',G,1)
    top=155; cw=186; ch=115; gapx=8; gapy=5
    for i,(tag,date,src,head) in enumerate(S):
        row,col=divmod(i,5); x=24+col*(cw+gapx); y=top+row*(ch+gapy)
        box(x,y,cw,ch,C);box(x,y,cw,3,R if i<5 else B)
        txt(x+8,y+8,tag,R,1,27)
        box(x+8,y+20,44,1,(211,207,197))
        lines=wrap(head,27)[:4]
        for j,line in enumerate(lines): txt(x+8,y+28+j*11,line,K,1,27)
        txt(x+8,y+75,'SOURCE / '+date,G,1,27)
        txt(x+8,y+88,src,G,1,27)
        txt(x+8,y+101,'DATE CHECKED',B,1,27)
    fy=top+6*(ch+gapy)+3
    box(24,fy,976,2,K)
    txt(30,fy+9,'THE WIRE  |  25 NOVEMBER 2026  |  SOURCES: REUTERS, ANADOLU, FT AND OTHERS',G,1)
    txt(30,fy+22,'DATES UNDER EACH HEADLINE REFER TO THE CITED REPORTING IN FACTS.MD',G,1)
    scan=bytearray()
    stride=W*3
    for yy in range(H): scan.append(0);scan.extend(img[yy*stride:(yy+1)*stride])
    def chunk(k,d):
        q=k+d
        return struct.pack('>I',len(d))+q+struct.pack('>I',zlib.crc32(q)&0xffffffff)
    data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(scan,7))+chunk(b'IEND',b'')
    dest=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
    os.makedirs(os.path.dirname(dest) or '.',exist_ok=True)
    with open(dest,'wb') as f:f.write(data)
    print('wrote',dest,len(data),'bytes')

if __name__=='__main__': main()
