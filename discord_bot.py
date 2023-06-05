from time import sleep
from selenium import webdriver
import discord
from discord.ext import commands, tasks
import logging
import time

import parser_funcs
import data
logging.basicConfig(level=logging.INFO, filename="log.log",filemode="w", format='%(asctime)s %(message)s')

token = data.discord['token']
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents=intent)

channel_id = data.discord['channel_id']

@bot.command(pass_context=False)
async def check(ctx):
    flag = False
    await ctx.send('падажди')
    out = parser_funcs.check(data=data.data, silent=False)
    if out:
        with open('tabel.html') as old_tabel:
            if out['tabel'] == old_tabel.read():
                await ctx.send('всё как было', file = discord.File("out.png"))
                logging.info(f"проверка: нет новых данных")
                print(f"проверка: нет новых данных")
            else:
                await ctx.send('чёт новое', file = discord.File("out.png"))
                logging.info(f"проверка: новые данные")
                print(f"проверка: новые данные")
                flag = True
        if flag:
            with open('tabel.html','w') as table:
                table.write(out['tabel'])
    else:
        logging.error('проверка: кака ято ошибка')
        print('проверка: кака ято ошибка')
        await ctx.send('Ошибка')
    
@bot.command(pass_context=True)        
async def start(ctx, arg1, arg2):
    try:
        minutes, silent = int(arg1), arg2 == 'True'
    except:
         await ctx.send(f"чёт вввёл криво")
    logging.info(f"начало цикла проверки каждые {minutes} минут в {'тихом режиме' if silent else 'обычном режиме'}")
    print(f"начало цикла проверки каждые {minutes} минут в {'тихом режиме' if silent else 'обычном режиме'}")
    check_site.start(ctx, minutes, silent)
    await ctx.send(f"Проверка баллов каждые {minutes} минут в {'тихом режиме' if silent else 'обычном режиме'}")

@bot.command(pass_context=False)
async def stop(ctx):
    check_site.stop()
    logging.info('цикл остановлен')
    print('цикл остановлен')
    await ctx.send('цикл остановлен')  
    
@tasks.loop(seconds=1)
async def check_site(ctx, minutes, silent):
    check_site.change_interval(minutes=minutes)
    flag = False
    out = parser_funcs.check(data=data.data, silent=True)
    if out:
        with open('tabel.html') as old_tabel:
            if out['tabel'] == old_tabel.read():
                if not silent: await ctx.send('всё как было', file = discord.File("out.png"))
                logging.info(f"цикличная проверка: нет новых данных")
                print(f"цикличная проверка: нет новых данных")
            else:
                await ctx.send('вау новое появилось', file = discord.File("out.png"))
                await ctx.send('🙃', file = discord.File(out['image']))
                logging.info(f"цикличная проверка: новые данные")
                print(f"цикличная проверка: новые данные")
                flag = True
        
        if flag:
            with open('tabel.html','w') as table:
                table.write(out['tabel'])
    else:
        check_site.stop()
        logging.error('цикличная проверка: кака ято ошибка')
        print('цикличная проверка: кака ято ошибка')
        await ctx.send('Ошибка')


if __name__ == "__main__":
    bot.run(token)