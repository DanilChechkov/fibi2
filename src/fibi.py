#!/usr/bin/env python3
import os
import sys
import os.path
import pickle
import vk_api
import random
import datetime
import time
import threading
from subprocess import Popen
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

#ЗАГРУЖАЕМ ТОКЕН
path = os.getcwd() +'/'
print(path)
token = open(path +'token').readline().rstrip()
print('\nToken:\t',token)
print('Variables creating...')
#СОЗДАЕМ ПЕРЕМЕННУЮ С ВРЕМЕННЫМИ ДАННЫМИ ПОЛЬЗОВАТЕЛЯ
idtemp = {'action':'intro','langs':{}}
wtfst = {}
#РЕДАКТИРОВАТЬ --> текст клавиатуры
chname, addlan, dellan = 'Я поменяль имя','Добавить язык','Удалить язык'
chlang, ediwor, delwor  = 'Очепятка в языке','Изменить слово','Удалить слово'
icmind = 'Я передумаль, Фиби=('
love,evol = 'Любовь-Love','Love-Любовь'
tss = 0
print('Keyboards creating...')
#СОЗДАЕМ КЛАВИАТУРУ СТОП
stopk = VkKeyboard(one_time=False)
stopk.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ГЛАВНОГО МЕНЮ
adwords,shwords,chwords,edwords = 'Пополнить словарь','Мой словарь','Проверь слова, Фиби!=)','Редактировать'
reminme = 'Напомни мне'
Mkeyboard = VkKeyboard(one_time=False)
Mkeyboard.add_button(adwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_button(shwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(chwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(reminme,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(edwords,color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ МЕНЮ РЕДАКТИРОВАНИЯ
editk = VkKeyboard(one_time=False)
editk.add_button(chname,color=VkKeyboardColor.POSITIVE)
editk.add_line()
editk.add_button(addlan,color=VkKeyboardColor.POSITIVE)
editk.add_button(dellan,color=VkKeyboardColor.NEGATIVE)
editk.add_line()
editk.add_button(chlang,color=VkKeyboardColor.POSITIVE)
editk.add_line()
editk.add_button(adwords,color=VkKeyboardColor.POSITIVE)
editk.add_button(delwor,color=VkKeyboardColor.NEGATIVE)
editk.add_line()
editk.add_button(icmind,color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ВЫБОРА ТИПА ПРОВЕРКИ
chtkey = VkKeyboard(one_time=False)
chtkey.add_button(love,color=VkKeyboardColor.POSITIVE)
chtkey.add_line()
chtkey.add_button(evol,color=VkKeyboardColor.POSITIVE)
chtkey.add_line()
chtkey.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ВЫБОРА СЛОВ ДЛЯ ПРОВЕРКИ
chtkey2 = VkKeyboard(one_time=False)
chtkey2.add_button('Все слова',color=VkKeyboardColor.POSITIVE)
chtkey2.add_line()
chtkey2.add_button('Последние n',color=VkKeyboardColor.POSITIVE)
chtkey2.add_line()
chtkey2.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#CОЗДАЕМ КЛАВИАТУРУ ВЫБОРА ДНЯ ДЛЯ НАПОМИНАНИЯ
remik = VkKeyboard(one_time=False)
remik.add_button('Сегодня',color=VkKeyboardColor.POSITIVE)
remik.add_button('Завтра',color=VkKeyboardColor.POSITIVE)
remik.add_line()
remik.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
print('Connecting...')
#ПОДКЛЮЧАЕМСЯ К VK
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
print('Function initialization...')

class WriteFirst:#СОЗДАЕМ ОТДЕЛЬНЫЙ ПОТОК ДЛЯ ФУНКЦИИ "ПИШУ ПЕРВОЙ" И "НАПОМНИ МНЕ"
    def __init__(self,interval = 60):
        self.interval = interval
        thread = threading.Thread(target=self.chkTi,args=())
        thread.daemon = True
        thread.start()

    def chkTi(self):
        global tss
        while True:
            nowt = datetime.datetime.now()
            dtm = [nowt.month,nowt.day,nowt.hour,nowt.minute]
            print(nowt.strftime('%d-%m-%Y\t%H:%M'))
            #WRITEFIRST
            try:
                tss += 1
                wtf = pload('writefirst')
                if tss == 90:
                    newmes(214708790,'All good!')
                    tss = 0
                for uid in wtf.keys():
                    if (dtm[0]>wtf[uid][0] or dtm[1]>wtf[uid][1]) and (dtm[2] >= wtf[uid][2] and dtm[3] > wtf[uid][3]):
                            wtf[uid]=dtm
                            pdump('writefirst',wtf)
                            tempu = pload(uid)
                            ch = {'%':0,'chkt':1,'chch':'!!!ВСЕ!!!','action':'chwords1'}
                            for key in ch.keys():
                                tempu[key] = ch[key]
                            pdump(uid,tempu)
                            x = tempu['langs'][min(tempu['langs'])]
                            out = 'Мы не общались больше суток, %s! Я тебе больше не нужна?=(\nСыграем? Загадай число от 1 до %d'%(tempu['uname'],len(x))
                            newmes(uid,out,stopk)
            except:
                print('NO DB YET')
            #НАПОМИНАНИЯ
            if os.path.isfile(path + 'reminder.pkl'):
                tmpr = pload('reminder')
                for reminder in tmpr[:]:
                    remdat = reminder[0:4]
                    if dtm[0]==remdat[0] and dtm[1]==remdat[1]:
                        if (dtm[2]==remdat[2] and dtm[3]>=remdat[3]) or (dtm[2]>remdat[2]):
                            for text in ('Эй',reminder[-1],'Нужно было напомнить.'):newmes(reminder[-2],text)
                            tmpr.remove(reminder)
                pdump('reminder',tmpr)
            else: 
                print('NO REMINDERS YET')
            time.sleep(self.interval)

def formdict(uid,idtemp, i=0,out =''): #ПОСТРОЕНИЕ МАССИВА СЛОВ ДЛЯ ОПРОСА
    try:
        idtemp['dict'] = []
        for language in idtemp['langs']:
            if idtemp['chch'] != '!!!ВСЕ!!!': language = idtemp['chch']
            for elem in enumerate(idtemp['langs'][language][::-1]):
                if i and i==elem[0]: break
                elem2 = elem[1][:]
                elem2.append(language)
                idtemp['dict'].append(elem2)
            if idtemp['chch'] != '!!!ВСЕ!!!':break
        #ПОДГОТОВКА К ИГРЕ И ФОРМИРОВАНИЕ ОТВЕТА
        if not i: out = 'Любишь сложнее, да, %s?\n'%idtemp['uname']
        random.shuffle(idtemp['dict'])
        idtemp['stlen'],idtemp['action'] = len(idtemp['dict']),'PLAYN'
        out += 'Я буду писать тебе слово, ты будешь писать ответ, мы подсчитаем процент правильных ответов вместе! Ты сможешь!)'
        out +='\nВсего слов: %s'%idtemp['stlen']
        newmes(uid,out)
        newmes(uid, 'Я начинаю: %s(%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2]) ,stopk)
    except:
        newmes(uid,'Oops... Broken x(')#,Mkeyboard)
    return idtemp

def formanswer(uid,message): #ФУНКЦИЯ ФОРМИРОВАНИЯ ОТВЕТОВ
    try:
        global idtemp, wtfst
        tempOUT = ''
        tempKEY = None
        now = datetime.datetime.now()
        ptu = path + str(uid) +'.pkl'
        print(now.strftime('%d-%m-%Y\t%H:%M'),"Chpon'k",sep='\t')
        #ПЫТАЕМСЯ ЗАГРУЗИТЬ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ С ЛОКАЛЬНОГО ХРАНИЛИЩА
        if os.path.isfile(ptu):idtemp = pload(uid)
        else: idtemp = {'action':'intro','langs':{}}

        if idtemp['action'] == 'mainmenu':#ОБНУЛЕНИЕ ИГРОВЫХ ПЕРЕМЕННЫХ
            ch0 = {'chkt':2,'%':0,'stlen':0,'chch':'NONE','remi':'','dict':[]}
            for key in ch0.keys(): idtemp[key] = ch0[key]
        
        if message.lower() in ['start','начать','привет']:#ЗНАКОМСТВО
            idtemp['uid'] = uid
            idtemp['action'] = 'intro0'
            tempOUT = ('Привет, меня зовут Фиби и я буду твоим персональным помощником в изучении языка. ' +
                    'Мы с тобой будем учить слова и с этого дня я от тебя не отцеплюсь! =)' +
                    'Я представилась, а как обращаться к тебе?)')
        
        elif message == shwords:#ПОКАЖИ МОЙ СЛОВАРЬ
            tempOUT = 'Хорошо, вот твой словарь, %s:\n'%idtemp['uname']
            count = 0  
            for lang in idtemp['langs'].keys():
                count += len(idtemp['langs'][lang])
                tempOUT += '\n%s (слов - %d):\n'%(lang,len(idtemp['langs'][lang]))
                for word in idtemp['langs'][lang]:
                    if len(tempOUT) >= 3800:
                        newmes(uid,tempOUT)
                        tempOUT = ''
                    tempOUT += '%s-%s\n'%(word[0],word[1])
            tempOUT += '\nВсего слов - %d'%count

        elif message == adwords:#ПОПОЛНИТЬ СЛОВАРЬ
            idtemp['action'] = 'adwords'
            tempOUT = 'Окей, но всё по порядку, %s =) Какой язык?'%idtemp['uname']
            tempKEY = buildkey(1,idtemp['langs'])
        #ПОПОЛНИТЬ СЛОВАРЬ|УДАЛИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВО --> ВЫБОР СЛОВАРЯ
        elif (message in idtemp['langs'].keys() or message =='!!!ВСЕ!!!') and idtemp['action'] in ('adwords','dellan','chlang','chwords0'):
            if idtemp['action'] == 'dellan':idtemp['langs'].pop(message) 
            ch1 = {  'adwords':(message,'Хорошо, отправляй мне по одному слову за сообщение, вот пример: Похмелье-Hang over. Не отделяй тире пробелами, пожалуйста=)',stopk,'NONE'),
                    'dellan':('mainmenu','Удалила =)',Mkeyboard,'NONE'),
                    'chlang': ('chlang0'+message,'На что меняем?',Mkeyboard,'NONE'),
                    'chwords0':('chwords1','Замечательный выбор!',chtkey2,message)}
            res,tempOUT,tempKEY,idtemp['chch'] = ch1[idtemp['action']]
            idtemp['action'] = res    
        #ПОПОЛНИТЬ СЛОВАРЬ| ПРОВЕРЬ МЕНЯ --> ВЫХОД В ГЛАВНОЕ МЕНЮ
        elif message in (icmind,'Стоп!') and idtemp['action'] in ('adwords','chwords','chwords0','chwords1',
            'PLAYN','edwords0','dellan','chlang', 'remme0','remme1','remme2'):
            ch = {  'adwords':('mainmenu','Окей, я готова двигаться дальше!=)',Mkeyboard),
                    'dellan':('edwords0','Ок, вернулись=)',editk),
                    'chwords0':('chwords','Ладно, шаг назад.',chtkey),
                    'chwords1':('chwords0','Серьезно?=(',buildkey(0,idtemp['langs'])),
                    'PLAYN':('chwords1','Ладно.',chtkey2)}
            ch['chwords']=ch['edwords0']=ch['remme0']=ch['remme1']=ch['remme2']=ch['adwords']
            ch['chlang']=ch['dellan']
            res,tempOUT,tempKEY = ch[idtemp['action']]
            idtemp['action'] = res
            
        elif message == edwords:#РЕДАКТИРОВАТЬ
            idtemp['action'] = 'edwords0'
            tempOUT = 'Что меняем, %s?'%idtemp['uname']
            tempKEY = editk
        elif message == chname and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> ПОМЕНЯЙ ИМЯ
            idtemp['action'] = 'introO'
            tempOUT = 'Как теперь мне тебя называть?=)'
            tempKEY = Mkeyboard
        elif message == addlan and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> ДОБАВИТЬ ЯЗЫК
            idtemp['action'] = 'introI'
            tempOUT = ('Давай добавим, %s! '%idtemp['uname'] +
                    'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
            tempKEY = Mkeyboard
        #РЕДАКТИРОВАТЬ --> УДАЛИТЬ ЯЗЫК|ОПЕЧАТКА В НАЗВАНИИ ЯЗЫКА
        elif message in (dellan,chlang) and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'dellan' if message == dellan else 'chlang'
            tempOUT = 'Какой язык удаляем?' if message == dellan else 'Какой язык изменяем, %s?'%idtemp['uname']
            tempKEY = buildkey(1,idtemp['langs'])
        elif message == delwor and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
            idtemp['action'] = 'delwor'
            tempOUT = 'Хорошо, %s, что мне удалить? Напиши по примеру: Похмелье-Hang over'%idtemp['uname']
            tempKEY = Mkeyboard
        
        elif message == chwords:#ПРОВЕРЬ МЕНЯ
            idtemp['action'] = 'chwords'
            tempOUT = 'Ок, %s. Как реализуем проверку? Есть два варианта:\n1) Я пишу тебе слово, а ты мне перевод.(любовь-love)\n2) Я пишу перевод, а ты мне слово.(love-любовь).'%idtemp['uname']
            tempKEY = chtkey
        elif message in (love,evol) and idtemp['action'] == 'chwords':#ПРОВЕРЬ МЕНЯ --> ВЫБОР ЯЗЫКА
            idtemp['chkt'] = 0 if message==love else 1
            idtemp['action'] = 'chwords0'
            tempOUT = 'Какой язык?'
            tempKEY = buildkey(0,idtemp['langs'])
        #ПРОВЕРЬ МЕНЯ --> ВЫБОР КОЛ-ВА слов
        elif (message in ('Все слова','Последние n') or message.isdigit()) and idtemp['action'] == 'chwords1':
            if message == 'Все слова': idtemp = formdict(uid,idtemp)
            elif message == 'Последние n':
                x = idtemp['langs'][min(idtemp['langs'])] if idtemp['chch'] == '!!!ВСЕ!!!' else idtemp['langs'][idtemp['chch']]
                tempOUT = 'Отличный выбор, %s!\nСколько слов? ответь цифрой 1 до %d'%(idtemp['uname'],len(x))
                tempKEY = stopk
            elif message.isdigit(): idtemp = formdict(uid,idtemp,int(message))
        elif message == reminme:#ОБНОВЛЕНИЕ 1. НАПОМНИТЬ МНЕ
            idtemp['action'] = 'remme0'
            tempOUT = 'О чем тебе напомнить, %s?'%idtemp['uname']
            tempKEY = stopk

        elif message[0:7].lower() == 'спасибо' and idtemp['action'] == 'mainmenu':
            tempOUT = random.choice(open(path+'welcome','r').readlines())

        elif message == 'show1': #ПЕРЕПИСАТЬ!!!ВЫВОД ВСЕХ ДАННЫХ В СООБЩЕНИИ
            print(idtemp)
            print(pload('reminder'))
        elif message == 'restart1': #ПЕРЕЗАГРУЗКА
            idtemp['action'] = 'mainmenu'
            for text in ('Чинюсь...','Исправление пространства времени...','Найдена доступная ячейка, подгружаюсь...','ASDmiqwjfndasiuNASUYHDLWdoasmdofmaoedwSSSASDWЙЦвыфываЯЛДФЫ'):
                newmes(uid,text)
            tempOUT = '!!!OK!!!'
            tempKEY = Mkeyboard
        else:
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> ПРОСИМ ВВЕСТИ ПОЛЬЗОВАТЕЛЯ ИЗУЧАЕМЫЕ ЯЗЫКИ|СОХРАНЯЕМ ИМЯ
            if idtemp['action'] in ('intro0','introO'):
                idtemp['uname'] =  message
                if idtemp['action'] == 'intro0':
                    idtemp['action'] = 'intro1'
                    tempOUT = ('Очень приятно, %s, Какие языки мы будем изучать?'%idtemp['uname'] +
                        'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
                else:
                    idtemp['action'] = 'mainmenu'
                    tempOUT = 'Хорошо, %s'%idtemp['uname']
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> СОХРАНЯЕМ ЯЗЫКИ КОТОРЫЕ ИЗУЧАЕТ ПОЛЬЗОВАТЕЛЬ
            elif idtemp['action'] in ('intro1','introI'):
                for lang in message.split(' '):idtemp['langs'][lang] = []
                idtemp['action'] = 'mainmenu'
                tempOUT = 'Замечательный выбор, а теперь смотри что я умею!' if idtemp['action']=='intro1' else 'Добавила =)'
                tempKEY = Mkeyboard
            elif idtemp['action'] in idtemp['langs'].keys(): #ПОПОЛНЕНИЕ СЛОВ
                if message == 'Стоп!':#ПОПОЛНЕНИЕ СЛОВ --> ПОЛЬЗОВАТЕЛЬ ЗАКОНЧИЛ ПОПОЛНЯТЬ СЛОВА
                    idtemp['action'] = 'adwords'
                    tempOUT = 'Добавим для другого языка, или всё?'
                    tempKEY = buildkey(1,idtemp['langs'])
                else:#ПОПОЛНЕНИЕ СЛОВ --> ДОБАВЛЯЕМ СЛОВА В СПИСОК
                    idtemp['langs'][idtemp['action']].append([message.split('-')[0].lower(), message.split('-')[1].lower()])
                    tempOUT = 'Ага, записала...'
                    tempKEY = stopk
            elif idtemp['action'][:7] == 'chlang0':#РЕДАКТИРОВАТЬ --> ИСПРАВЛЯЕМ НАЗВАНИЕ ЯЗЫКА
                idtemp['langs'][message] = idtemp['langs'].pop(idtemp['action'][7:])
                idtemp['action'] = 'mainmenu'
                tempOUT = 'Готово!=)'
                tempKEY = Mkeyboard
            elif idtemp['action'] == 'delwor':#РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
                for language in idtemp['langs']:
                    try:
                        idtemp['langs'][language].remove(message.lower().split('-'))
                        tempOUT = 'Удалила!=)';break
                    except:tempOUT = 'Упс=( Не могу найти слова. Напиши точно так же как в твоем словаре, пожалуйста!'
                idtemp['action'] = 'mainmenu'
                tempKEY = Mkeyboard
            #ПРОВЕРЬ МЕНЯ --> ПОЛЬЗОВАТЕЛЬ ВВОДИТ СЛОВО
            elif idtemp['action'] == 'PLAYN':
                #ПРАВИЛЬНО ОТВЕТИЛ
                if message.lower() in idtemp['dict'][0] and message != idtemp['dict'][0][idtemp['chkt']]:
                    tempOUT = 'Правильно!'
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    tempOUT += '\nТочность: %.2f'%cur
                    if len(idtemp['dict'])>1:#СЛОВА ЕЩЁ ЕСТЬ
                        idtemp['dict'].remove(idtemp['dict'][0])
                        tempOUT += '\nНовое слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
                        tempKEY = stopk
                    else:#ПОСЛЕДНЕЕ СЛОВО
                        idtemp['action']='mainmenu'
                        cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                        tempOUT = 'Поздравляю %s, мы закончили!=)\nТвой результат: %.2f'%(idtemp['uname'],cur)
                        tempKEY = Mkeyboard
                else:#НЕПРАВИЛЬНО ОТВЕТИЛ
                    idtemp['%'] +=1
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    tempOUT = 'Ошибка! Точность: %.2f'%cur
                    tempKEY = stopk
                    tempOUT += '\nПостарайся ещё, слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
            elif idtemp['action'] == 'remme0':#НАПОМНИ МНЕ --> ВЫБОР ДАТЫ
                idtemp['action'] = 'remme1'
                idtemp['remi'] = [message]
                tempOUT = "Супер, записала, теперь укажи дату в формате %s, где день и месяц разделены пробелом.\nИли выбери на клавиатуре"%now.strftime('%d %m')
                tempKEY = remik
                #tempOUT = "Отлично, теперь укажи дату в формате: %d.%d.%d.%d  где:\n%d - Месяц\n%d - Число\n%d - Час\n%d - Минута\nНе используй нули и пробелы а то я запутаюсь =("%(now.month,now.day,now.hour,now.minute,now.month,now.day,now.hour,now.minute)
            elif idtemp['action'] == 'remme1':#НАПОМИНАНИЕ --> ЗАПОМНИТЬ ДАТУ
                idtemp['action'] = 'remme2'
                if message.lower() == "сегодня":
                    idtemp['remi'].append(now.month)
                    idtemp['remi'].append(now.day)
                elif message.lower() == "завтра":
                    tomorrow = now + datetime.timedelta(days=1)
                    idtemp['remi'].append(tomorrow.month)
                    idtemp['remi'].append(tomorrow.day)
                elif message[-1:].isdigit():
                    dt = [int(x) for x in message.split()]
                    idtemp['remi'].append(dt[1])
                    idtemp['remi'].append(dt[0])
                tempOUT = "А теперь укажи время дня в формате %s, где час и минута разделены пробелом."%now.strftime('%H %M')
                tempKEY = stopk
            elif idtemp['action'] == 'remme2': #НАПОМИНАНИЕ --> ЗАПОМНИТЬ ВРЕМЯ
                idtemp['action'] = 'mainmenu'
                dt = [int(x) for x in message.split()]
                idtemp['remi'].append(dt[0])
                idtemp['remi'].append(dt[1])
                ptr = path + 'reminder.pkl'
                if os.path.isfile(ptr):tmpr = pload('reminder')
                else: tmpr = []
                z = idtemp['remi'][1:]
                z.append(uid)
                z.append(idtemp['remi'][0])
                tmpr.append(z)
                tmpr.sort()
                print(tmpr)
                pdump('reminder',tmpr)
                tempOUT,tempKEY ='Хорошо, %s. Я напомню'%idtemp['uname'], Mkeyboard

        #WRITING A NEW MESSAGE
        if tempOUT:
            if tempKEY: newmes(uid,tempOUT,tempKEY)
            else: newmes(uid,tempOUT)
        #WRITEFIRST
        ptw = path + 'writefirst.pkl'
        if os.path.isfile(ptw):wtfst = pload('writefirst')
        wtfst[uid] = [now.month,now.day, now.hour,now.minute]
        pdump('writefirst',wtfst)
        pdump(uid,idtemp)
    except SystemExit: sys.exit(0)
    except: newmes(uid,'Oops...(Try restart1)')

def buildkey(type0,langs=None): #ФУНКЦИЯ ПОСТРОЕНИЯ КЛАВИАТУРЫ
    keyboard = VkKeyboard(one_time=False)
    for x in enumerate(langs.keys()):
        if x[0]%2==0 and x[0]>1: keyboard.add_line()
        keyboard.add_button(x[1],color=VkKeyboardColor.POSITIVE)
    if not type0:
        keyboard.add_line()
        keyboard.add_button('!!!ВСЕ!!!',color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
    return keyboard

def newmes(uid,message,*keyboard): #ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ
    if keyboard:
        vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),
                                'message':message,'keyboard':keyboard[0].get_keyboard()})
    else:vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),'message':message})

def pdump(uid,idtem): #ФУНКЦИЯ СОХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ НА ДИСК
    with open(path + str(uid)+'.pkl','wb') as f: pickle.dump(idtem,f)
def pload(uid): #ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ ПОЛЬЗОВАТЕЛЯ С ДИСКА 
    with open(path + str(uid)+'.pkl','rb') as f: return pickle.load(f)

print('Second thread creating...')
wt=WriteFirst()
print('System ready')
newmes(214708790,'System ready!')
while True:#ПОЛУЧАЕМ НОВЫЕ СООБЩЕНИЯ В ЦИКЛЕ
    try:
        for event in longpoll.listen():
            if event.to_me:
                if event.type == VkEventType.MESSAGE_NEW: formanswer(event.user_id,event.text)
    except SystemExit: break
    except: print('SYSTEM FUCKED UP')