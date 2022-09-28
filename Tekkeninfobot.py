from email import message
from enum import Flag
from itertools import cycle
from multiprocessing import Value
from sqlite3 import Timestamp
from turtle import clear, title
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import csv

#출력 리스트 정의
keylist = [] #key 리스트
vallist = [] #value 리스트
fname = [] #프레임표 이름 리스트

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) #접두사
token = os.environ['token']
bot.remove_command('help')

#커맨드 이모지
ID1 = "<:1_:1024564982567940116>" #스틱 1
ID1H = "<:1H:1024565057943777300>" #스틱 1 H
ID2 = "<:2_:1024565125086195773>" #스틱 2
ID2H = "<:2H:1024565138839326760>" #스틱 2 H
ID3 = "<:3_:1024565598551822356>" #스틱 3
ID3H = "<:3H:1024565166286839808>" #스틱 3 H
ID4 = "<:4_:1024565179784122408>" #스틱 4
ID4H = "<:4H:1024565190542503996>" #스틱 4 H
IDN = "<:5_:1024565203473547297>" #스틱 중립
ID6 = "<:6_:1024565216110968832>" #스틱 6
ID6H = "<:6H:1024565229448876053>" #스틱 6 H
ID7 = "<:7_:1024565242031788052>" #스틱 7
ID7H = "<:7H:1024565259983388672>" #스틱 7 H
ID8 = "<:8_:1024565261682102363>" #스틱 8
ID8H = "<:8H:1024565263405961226>" #스틱 8 H
ID9 = "<:9_:1024565265297584168>" #스틱 9
ID9H = "<:9H:1024565346356699226>" #스틱 9 H
ILP = "<:LP:1024565378749321236>" #버튼 LP
IRP = "<:RP:1024565393190305825>" #버튼 RP
ILK = "<:LK:1024565374529847338>" #버튼 LK
IRK = "<:RK:1024565389797097554>" #버튼 RK
IAP = "<:AP:1024565352950153217>" #버튼 AP
IAK = "<:AK:1024565349431115776>" #버튼 AK
IAL = "<:AL:1024565351154991176>" #버튼 AL
IAR = "<:AR:1024565358847328286>" #버튼 AR
ILR = "<:LR:1024565382113148938>" #버튼 LP+RK
IRL = "<:RL:1024565391755853854>" #버튼 RP+LK
IPL = "<:APLK:1024565355349278790>" #버튼 AP+LK
IPR = "<:APRK:1024565357022806016>" #버튼 AP+RK
IKL = "<:LPAK:1024565380389273620>" #버튼 LP+AK
IKR = "<:RPAK:1024565394985455627>" #버튼 RP+AK
IAB = "<:AB:1024565347925381190>" #버튼 AB
IRA = "<:Rage:1024565894493524009>" #레이지
IWs = "<:Ws:1024565902101970954>" #일어나며
IHo = "<:HOLD:1024565887795216455>" #홀드

#기술 옵션
S_Rage = 0xff0000 #레이지
S_S = 0x1a7e00    #스크류기
S_A = 0x9258bd    #시동기
S_Tss = 0x0079fd  #호밍기
S_Pc = 0xce0000   #파워크래시
S_Wb = 0xf66800   #월바운드
S_Wsr = 0xf6e1aa  #벽비틀
S_N = 0x2f3136    #일반기술

#판정 이모지
J_H = "<:high:1024565885798727730>" #상단
J_M = "<:middle:1024565891385540638>" #중단
J_L = "<:low:1024565889565208597>" #하단
J_unb = "<:unb:1024565900235522068>" #가드 불능 기술
J_C = "<:catch:1024565905671331840>" #잡기
J_D = "<:down:1024565908045316146>" #다운
J_pun = "<:pun:1024565892983558185>" #타격
J_smid = "<:smiddle:1024565896586465290>" #특중
J_special = "<:special:1024565898209665095>" #특수
bl = "<:blank:1024565903968440320>" #빈칸

playing = cycle(["!도움", "!명령어", "!검색"]) #상태창 배열

#상태창 변화 함수
@tasks.loop(seconds=3) #간격 설정
async def chanhe_status():
    await bot.change_presence(activity=discord.Game(next(playing)))

#봇 연결 출력
@bot.event
async def on_ready():
    chanhe_status.start()
    print("########봇 연결 완료.(connected)########")

#도움
@bot.command()
async def 도움(ctx):
    embed=discord.Embed(title="안내", color=0x5865f2, timestamp=ctx.message.created_at)
    embed.add_field(name="!도움", value="도움", inline=False)
    embed.add_field(name="!ping", value="봇 응답상태 확인", inline=False)
    embed.add_field(name="!명령어", value="명령어 목록", inline=False)
    embed.set_footer(text="개발자 - @황소2020#2020")
    await ctx.send(embed=embed)

#ping
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

#명령어
@bot.command(aliases = ["명령", "커맨드"])
async def 명령어(ctx):
    embed=discord.Embed(title="멸령어", color=0x5865f2, timestamp=ctx.message.created_at)
    embed.add_field(name="!도움", value="도움", inline=False)
    embed.add_field(name="!ping", value="봇 응답상태 확인", inline=False)
    embed.add_field(name="!명령어", value="명령어 목록", inline=False)
    embed.add_field(name="!검색 [캐릭터명] [기술명]", value="해당 캐릭터의 기술정보", inline=False)
    embed.add_field(name="!캐릭터", value="검색할 수 있는 캐릭터 목록", inline=False)
    embed.set_footer(text="개발자 - @황소2020#2020")
    await ctx.send(embed=embed)


#검색
@bot.command(aliases = ["기술", "프레임", "f", "검"])
async def 검색(ctx, cname, sname):
    cercode = 1 #에러 발송 여부 초기화
    k=0 #검색횟수 제한 초기화
    
    #프레임표 이름 불러오기
    flist = os.listdir('Commandlists') #파일경로
    fname.clear() #다시 불러오는 경우를 위해 리스트 초기화
    for f_i in flist:
        fname.append(str(os.path.splitext(f_i)[0])) #파일명 확장자 제거해서 fname리스트에 추가

    #캐릭명 자동완성(대체이름과 킹같은 단일 겹치는 이름 해결할 필요 있음)
    for ff_i in range(len(fname)):
        if str(cname) in fname[ff_i]:
            cercode = 1
            break
        else: #못찾은 경우
            cercode = 0
            ercode = 201

    if cercode == 0: #못찾은 경우 에러 발송
        if ercode == 201:
            embed=discord.Embed(title="Error 201", description="검색하신 캐릭터를 찾을 수 없습니다.", color=0xff0000)
            embed.set_footer(text="개발자 - @황소2020#2020")
            await ctx.send(embed=embed)

    if cercode == 1: #에러가 없을경우
        #입력한 캐릭명에 맞춰 해당 파일 data에 list로 저장
        path = "Commandlists/"+str(fname[ff_i])+".csv" #파일경로
        f = open(path, 'r') #파일명, 읽기모드
        rdr = csv.DictReader(f)
        data = list(rdr) #data에 cname캐릭터의 기술 딕셔너리를 리스트로 저장
        f.close()

    if cercode == 1: #에러가 없을경우
        for i in range(len(data)):
            for key, value in data[i].items():
                if str(sname) in data[i]["기술명"] or str(sname) in data[i]["대체기술명"]:
                    #호출한 기술이 6개 초과시 불러오기 무시
                    if k >= 6:
                        break
                    #호출시 출력 리스트에 추가
                    elif k <= 5:
                        keylist.append(list(data[i].keys())) #keylist에 일치하는 key 추가
                        vallist.append(list(data[i].values())) #vallist에 일치하는 value 추가
                        cercode = 1 #에러코드 발송 불필요
                        k = k + 1
                        break #임베드 발송시 for문 빠져나오기
                else:
                    if len(keylist) == 0:
                        cercode = 0 #에러 발송
                        ercode = 202 #맞는 기술명을 찾지 못함
        #출력
        if cercode == 1:
            #기술 출력
            embed=discord.Embed(title=str(fname[ff_i])+" - "+str(vallist[0][0]), description=str(vallist[0][1]), color=eval(vallist[0][2]))
            embed.add_field(name=keylist[0][3], value=eval(vallist[0][3]), inline=False)   #커맨드
            embed.add_field(name=keylist[0][4], value=eval(vallist[0][4]), inline=True)    #판정
            embed.add_field(name=keylist[0][5], value=vallist[0][5], inline=True)          #발동
            embed.add_field(name=keylist[0][6], value=vallist[0][6], inline=False)         #대미지
            embed.add_field(name=keylist[0][7], value=vallist[0][7], inline=True)          #가드
            embed.add_field(name=keylist[0][8], value=vallist[0][8], inline=True)          #히트
            embed.add_field(name=keylist[0][9], value=vallist[0][9], inline=True)          #카운터
            embed.add_field(name=keylist[0][10], value=eval(vallist[0][10]), inline=False) #비고
            embed.set_footer(text="개발자 - @황소2020#2020")
            await ctx.send(embed=embed)

            #연관검색어 출력
            if k >= 2:
                embed=discord.Embed(title="연관검색어", description=fname[ff_i]+"의 '"+sname+"'에관한 연관검색어", color=0x5865f2)
                for m in range(len(vallist)-1):
                    if m >= 11: #출력한 기술이 10개 초과시 출력 중지
                        embed.add_field(name="...", value="...")
                        break
                    embed.add_field(name=str(m+1)+". "+str(vallist[m+1][0]), value=eval(vallist[m+1][3]), inline=False)
                embed.set_footer(text="개발자 - @황소2020#2020")
                await ctx.send(embed=embed)

        elif cercode == 0:
            if ercode == 202:
                embed=discord.Embed(title="Error 202", description="검색하신 기술을 찾을 수 없습니다.", color=0xff0000)
                embed.set_footer(text="개발자 - @황소2020#2020")
                await ctx.send(embed=embed)

    keylist.clear() #리스트 초기화
    vallist.clear() #리스트 초기화

@bot.command(aliases=["캐릭"])
async def 캐릭터(ctx):

    #프레임표 이름 불러오기
    flist = os.listdir('Commandlists') #파일경로
    fname.clear() #다시 불러오는 경우를 위해 리스트 초기화
    for f_i in flist:
        fname.append(str(os.path.splitext(f_i)[0])) #파일명 확장자 제거해서 fname리스트에 추가

    embed=discord.Embed(title="캐릭터 목록", description="검색할 수 있는 캐릭터 목록", color=0x5865f2, timestamp=ctx.message.created_at)  
    for i in range(len(fname)):
        embed.add_field(name=fname[i], value="#완성도 추가 예정#", inline=True)
    await ctx.send(embed=embed)

bot.run(token)