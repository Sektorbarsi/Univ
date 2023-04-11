import discord
from discord import utils
import config

class MyClient(discord.Client):
# Проверка готовности бота
    async def on_ready(self):#Само включение бота провоцируюет
        print('Logged on as {0}!'.format(self.user))
# Добавление роли с помощью реакций
    async def on_raw_reaction_add(self, payload):# Нажатие или добовление реакции запускает процесс
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = payload.member # получаем объект пользователя который поставил реакцию
            print(member)
 
            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
            
                if(len([i for i in member.roles if i and True]) <= config.MAX_ROLES_PER_USER):# Проверка на количество и на роль админа(второе я убрал поэтому 
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
            
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
 
    async def on_raw_reaction_remove(self, payload):# удалении реации
        channel = self.get_channel(payload.channel_id) # получаем id канала
        message = await channel.fetch_message(payload.message_id) # получаем id сообщения
        user_id = payload.user_id
        member = await (await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
        print(member, user_id)
 
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)
    
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
 
# RUN
client = MyClient(intents = discord.Intents.all())
client.run(config.TOKEN)

#https://discordpy.readthedocs.io/en/stable/api.html
#Документация
