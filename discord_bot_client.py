import discord
import requests
import json
from discord.ext import commands
from datetime import datetime, time, timedelta
import calendar
import time
import asyncio
from pytz import timezone
import os
import sys
import random
import re
import pickle
import youtube_dl
import random
import validators
from youtube_search import YoutubeSearch
from carry_class import Carry
import dateparser 
from birthday import Birthdays
from nsfw_model.nsfw_detector import predict
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub

class MyClient(discord.Client):
    authorizedUsers = [132996207831285760]  # My ID
    quotes = []
    isUrsusTimeTurnOn = False

    async def send_birthday_notice(self):
        general_channel = self.guild.get_channel(751995980395839499)

        for birthday in self.birthdays.all_birthdays:
            if birthday.time_till == 0:
                try:
                    await general_channel.send(f'<@{birthday.user_id}> Happy Birthday!! <:UmbreonHappy:630381177076711425><:EspeonParty:630381017353682974><:UmbreonHYPE:630381573534908416>') 
                except Exception as e:
                    print(e)
            else:
                break

    def isUrsusTime(self):
        start_time1 = datetime.strptime('6:00 PM', '%I:%M %p').time()
        end_time1 = datetime.strptime('8:00 PM', '%I:%M %p').time()
        
        start_time2 = datetime.strptime('1:00 AM', '%I:%M %p').time()
        end_time2 = datetime.strptime('3:00 AM', '%I:%M %p').time()

        current_time = datetime.utcnow().time()

        between_first_interval = False
        between_second_interval = False
        if start_time1 < end_time1:
            between_first_interval = (current_time >= start_time1 and current_time <= end_time1)
        else: # Corsses midnight
            between_first_interval = (current_time >= start_time1 or current_time <= end_time1)


        if start_time2 < end_time2:
            between_second_interval = (current_time >= start_time2 and current_time <= end_time2)
        else: # Corsses midnight
            between_second_interval = (current_time >= start_time2 or current_time <= end_time2)
        
        return between_first_interval or between_second_interval

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        self.image_commands = {}
        for root, dirs, files in os.walk("commands"):
            for d in dirs:
                for sub_root, sub_dirs, sub_files in os.walk(f"commands/{d}"):
                    for name in sub_dirs:
                        self.image_commands[f">{name}"] = os.path.join(f"{root}/{d}", name)
        print(self.image_commands)
        self.carry_list = []
        #await self.scrap()
        self.birthdays = Birthdays()
        self.playing = False
        self.isUrsusTimeTurnOn = False
        self.carry_channel = [547026678438690836,737089087508447362,539516154625130496,736911310423326751,736392255421546517]
        self.carry_list = []
        self.guild = client.get_guild(671132975659745310)
        try:
            self.carry_list = pickle.load(open("carries.pickle","rb"))
            for carry in self.carry_list:
                if datetime.utcnow() < carry.when:
                    print(f"{carry.owner}'s carrie is resumed")
                    self.loop.create_task(self.create_new_carry(carry))
                else:
                    self.carry_list.remove(carry)
                    print("Removal")
                    print(f"One carry expired. Carry Owner is: {self.get_user(carry.owner).display_name}")
                    pickle_out = open("carries.pickle", "wb")
                    pickle.dump(self.carry_list, pickle_out)
        except:
            print("No pickle has been found")
        
        self.name_mapping = {}
       # print(self.guild.me.guild_permissions.manage_nicknames)
       # with open("name_mapping.txt", "r+") as fp:
       #     for member in self.guild.members:
       #         try:
       #             if member.nick == "HAPPY BIRTHDAY":
       #                 await member.edit(nick=None)
       #         except Exception as e:
       #             print(f"cannot change user {member.nick}")#
       #             print(e)

        with open("beautiful.txt", "r") as beautifuls:
            self.beautiful_list = [beautiful.strip("\n") for beautiful in beautifuls.readlines()]
        print('-----')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="You Sleep..."))

        #model = predict.load_model("./nsfw_model/mobilenet_v2_140_224/saved_model_old.h5")
        self.model = tf.keras.models.load_model('./nsfw_model/mobilenet_v2_140_224/saved_model.h5',custom_objects={'KerasLayer':hub.KerasLayer})
        print("done loading!")
        
    async def change_channel_name(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                #await self.get_channel(698038822809632768).edit(name=f"\U000023F0{datetime.utcnow().strftime('%a - %I:%M %p | UTC |')}")
                if datetime.utcnow().minute == 55 and datetime.utcnow().hour in [11, 18, 20, 21, 22]:
                    flag_race_str = "<:YayRoo:609639493288591371><:YayRoo:609639493288591371> Hey <@&698067878133628958>! Its going to be 5 minutes until " \
                                    "<:UmbreonHYPE:630381573534908416>**Flag Race**!!<:UmbreonHYPE:630381573534908416> " \
                                    "Dont forget to participate! <:sealwave:695186898230181949>"
                    #await self.get_channel(539219885922713623).send(flag_race_str, file=discord.File(f"gifs/{random.choice(os.listdir('gifs'))}"),delete_after = 360)
                if self.isUrsusTime() and self.isUrsusTimeTurnOn == False:
                    await self.get_channel(752691454467375104).edit(name="👉It's Ursus Time!👈")
                    #await self.get_channel(698056461002997760).edit(name="Ursus Time Under Maintenance")
                    self.isUrsusTimeTurnOn = True
                    print(f'Turning on UrsusTime. Currently {datetime.utcnow()}')
                elif self.isUrsusTime() == False and self.isUrsusTimeTurnOn == True:
                    self.isUrsusTimeTurnOn = False
                    print(f'Turning off UrsusTime. Currently {datetime.utcnow()}')
                    await self.get_channel(752691454467375104).edit(name="😔It's not Ursus Time")
                    #await self.get_channel(698056461002997760).edit(name="Ursus Time Under Maintenance")
                # Change_channel_name function now isnt truly a change_channel... this is now just a time check function.............. :(
                if datetime.utcnow().minute == 0 and datetime.utcnow().hour == 0:
                    self.birthdays = Birthdays()
                    await self.send_birthday_notice()
            except Exception as e:
                print(e)
                print("Change_channel errored")

            sleep_for = 60 - datetime.utcnow().second
            if sleep_for < 10:
                sleep_for = 60
            await asyncio.sleep(sleep_for)

    async def music_command(self, message):
        if message.author.voice.channel != None:
            if not discord.opus.is_loaded():
                discord.opus.load_opus('libopus.so')
            url = message.content.split(" ")[1]
            vc = None
            try:
                vc = await message.author.voice.channel.connect()
            except discord.ClientException:
                for voice in self.voice_clients:
                    if voice and voice.is_connected():
                        voice.stop()
                        vc = voice
            opts = {
                'cachedir': False,
                'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality':'4000'
                 }],
                 'outtmpl': 'song.mp3',
             }
            
            if not validators.url(url):
                results = json.loads(YoutubeSearch(message.content[6:], max_results=10).to_json())
                embed = discord.Embed(title="Search Results", description="Please Select A Number", color=0x00ff00)
                for i, r in enumerate(results['videos']):
                    embed.add_field(name=i+1, value =r['title'], inline=False)

                await message.channel.send(embed=embed)
                channel = message.channel
                author = message.author
                response = None
                try:
                    response = await self.wait_for('message', check=(lambda msg: msg.channel == channel and msg.author == author), timeout=12)
                    user_selection = int(response.content)
                    if not (1 <= user_selection <= len(results['videos'])):
                        raise ValueError("Incorrect selection")
                    url = 'https://www.youtube.com' + results['videos'][user_selection - 1]['link']
                except ValueError:
                    await message.channel.send("Incorrect selection")
                    return
                except asyncio.TimeoutError:
                    await message.channel.send("You took too long to answer!")
                    return
                except Exception as e:
                    print("Something happened here...")
                    print(e)
                    return
            with youtube_dl.YoutubeDL(opts) as ydl:
                try:
                    if os.path.exists('song.mp3'):
                        os.remove('song.mp3')
                    ydl.download([url])
                except FileNotFoundError:
                    pass
                except Exception as e:
                    print(f'Error occured in music... {e}')
                    await message.channel.send("Bad stuff happened :(")
            await message.channel.send("Playing...")
            vc.play(discord.FFmpegPCMAudio("song.mp3"))
            return

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.lower() in self.image_commands:
            if "restricted" in self.image_commands[message.content.lower()] and message.channel.id != 751995980395839499:
                await message.channel.send("Hey! This image content cannot be shown in this channel!")
                return
            image_selected = random.choice(os.listdir(self.image_commands[message.content.lower()]))
            path = f"{self.image_commands[message.content.lower()]}/{image_selected}"
            await message.channel.send(file=discord.File(path))

        if message.author.id == 132996207831285760: #Me:
            if message.content.lower().startswith(">play"):
                await self.music_command(message)

            if message.content.lower() == ">pause":
                for vc in self.voice_clients:
                    if vc and vc.is_playing():
                        vc.pause()

            if message.content.lower() == ">stop":
                for vc in self.voice_clients:
                    if vc and vc.is_playing():
                        vc.stop()

            if message.content.lower() == ">resume":
                for vc in self.voice_clients:
                    if vc and vc.is_paused():
                        vc.resume()

            if message.content.lower() == ">leave":
                for vc in self.voice_clients:
                    if vc and vc.is_connected():
                        await vc.disconnect()
        #if message.channel.id == 738886647059316838:
        #    await self.add_birthday(message)

        if message.content.lower() == ".birthdays":
            birthday_embed = discord.Embed(title="10 Upcoming Birthdays! (in UTC Timezone)", description="Watch out for these fellows with their birthdays nearing! Remember to wish em a happy early birthday!", color=0x42b9f5)
            for i in range(0, 10):
                b = self.birthdays.all_birthdays[i]
                member = client.get_guild(671132975659745310).get_member(b.user_id).display_name
                if b.time_till == 0:
                    birthday_embed.add_field(name=member, value=f"<:EspeonParty:630381017353682974> Today is his/her birthday! <:EspeonParty:630381017353682974>)", inline=False)
                else:
                    birthday_embed.add_field(name=member, value=f"in {b.time_till} days ({b.birthday_string})", inline=False)
            birthday_embed.set_footer(text="Happy Early Birthdays to these fellas!")
            await message.channel.send(embed=birthday_embed)

        if message.content.lower() == ".quit" and message.author.id in self.authorizedUsers:
            exit()
        
        if message.content.lower() == "still alive?" and message.author.id == 132996207831285760:
            await message.channel.send("Yes! Alive and well!")

        if (message.content.lower() == "no u" or message.content.lower() == "no you") and message.author.id != 132996207831285760:
            await message.channel.send("no u")

        if re.search(r'\bowo\b', message.content.lower()) and message.author.id != 132996207831285760:
            await message.channel.send("uwu")

        if re.search(r'\buwu\b', message.content.lower()) and message.author.id != 132996207831285760:
            await message.channel.send("owo")
        
        if message.content.lower().startswith(">stats"):
            try:
                int(message.content.split()[1])
            except:
                await message.channel.send("Please give me the user ID")
                return
            joined_date = message.guild.get_member(int(message.content.split()[1])).joined_at
            created_date = message.guild.get_member(int(message.content.split()[1])).created_at
            await message.channel.send(f"{message.guild.get_member(int(message.content.split()[1])).display_name} joined at {joined_date} UTC") 
            await message.channel.send(f"{message.guild.get_member(int(message.content.split()[1])).display_name} account was created at {created_date} UTC") 
        
        if message.channel.type == discord.ChannelType.private:
            await self.get_guild(671132975659745310).get_member(132996207831285760).send(f"Msg Received From {message.author.name}: {message.content}")

        if message.content.startswith(">send") and message.author.id == 132996207831285760:
            await self.get_guild(671132975659745310).get_member(int(message.content.split(" ")[1])).send(" ".join(message.content.split(" ")[2:]))
        
        #if message.content.lower().startswith(">carry"):
        #    await self.carry_command(message)
        
        #if message.content.lower().startswith(">cancel_carry"):
        #    await self.cancel_carry_command(message)

        if message.channel.id == 751995980395839499 and len(message.attachments) > 0:
            for attachment in message.attachments:
                await attachment.save("image_to_classify_if_nsfw.jpg")
                predicted_result = predict.classify(self.model, "image_to_classify_if_nsfw.jpg")
                res = predicted_result['image_to_classify_if_nsfw.jpg']
                print(res)
                if res["hentai"] >= 0.7 or res["porn"] >= 0.7:
                    await message.channel.send(f"<@{message.author.id}> The image you uploaded has been flagged as NSFW\n" +
                            f"Likelihood of Hentai: {res['hentai']}\n"+
                            f"Likelihood of Porn: {res['porn']}\n"
                            "Please keep this channel clean. If you think this is a inaccurate flag, please report to Snooted (Bin)")
                    await message.delete()

    async def cancel_carry_command(self, message):
        found_carry = None

        for carry in self.carry_list:
            if message.author.id == carry.owner and message.channel.id == carry.carry_id:
                found_carry = carry

        if found_carry == None:
            await message.channel.send("You have no active carry in this channel")
            return

        notify_str = f'<@{carry.owner}> has decided to cancel the {carry.carry_name} <:SealWant:704474834905858157><:SealWant:704474834905858157><:SealWant:704474834905858157> '
        for member in found_carry.member_list:
            notify_str += f'<@{member}>'

        await message.channel.send(notify_str)

        delete_message = await message.channel.fetch_message(carry.message_id)

        await delete_message.delete()
        self.carry_list.remove(carry)
        pickle_out = open("carries.pickle", "wb")
        pickle.dump(self.carry_list, pickle_out)
    
    async def carry_command(self, message):
        if message.channel.id not in self.carry_channel:
            await message.channel.send("Wrong Channel Bud")
            return

        for carry in self.carry_list:
            if carry.owner == message.author.id and carry.carry_id == message.channel.id:
                await message.channel.send("You already have an active carry roster going. Please cancel it before you start another one. To cancel, do .cancel_carry")
                return

        error_msg = "> Wrong Input Format. " \
                "\n> The correct format is >carry <TIME> minutes/hours" \
                "\n> Please specify a time until the start of the carry. For example:\n " \
                "> *If I am carrying 5 hours and 30 minutes from now, I would do:* " \
                "\n> **>carry 5 hours 30 minutes**\n> ***OR*** \n> **>carry 330 minutes**" \
                "\n> NOTE: minutes/hours must be spelled out completely as minutes and or hours. Using abbreviation would not work"
        sm = message.content.lower().split()
        if len(sm) < 3 or len(sm) > 5 or sm.count("minutes") > 1 or message.content.lower().split().count("hours") > 1:
            await message.channel.send(error_msg)
            return

        minutes = 0
        hours = 0
        try:
            minute_index = message.content.lower().split().index("minutes") - 1
            minutes = int(message.content.lower().split()[minute_index])
        except:
            pass

        try:
            hour_index = message.content.lower().split().index("hours") - 1
            hours = int(message.content.lower().split()[hour_index])
        except:
            pass

        if minutes == 0 and hours == 0:
            await message.channel.send(error_msg)
            return

        # Done Validation Up to this Point... I think I caught them all??
        start_time = datetime.utcnow() + timedelta(minutes = minutes, hours = hours)
        msg_to_delete = await message.channel.send("Creating Roster...")

        new_carry = Carry(owner = message.author.id, carry_id = message.channel.id, when = start_time, message_id = msg_to_delete)
        notification_str = "<:YayRoo:609639493288591371><:YayRoo:609639493288591371><:YayRoo:609639493288591371>"

        for ping_id in new_carry.channel_role_ping_id:
            notification_str += f"<@&{ping_id}>"

        await msg_to_delete.delete()

        notification_str += f" {message.author.nick} has started a {new_carry.carry_name}!<:LatiasLol:630381064749318144><:LatiasLol:630381064749318144><:LatiasLol:630381064749318144>"
        new_msg = await message.channel.send(notification_str)

        await new_msg.add_reaction("<:UmbreonHappy:630381177076711425>")

        new_carry.message_id = new_msg.id
        self.carry_list.append(new_carry)   
        pickle_out = open("carries.pickle", "wb")
        pickle.dump(self.carry_list, pickle_out)

        self.loop.create_task(self.create_new_carry(new_carry))


    async def create_new_carry(self, carry):
        while not self.is_closed() and datetime.utcnow() < carry.when and carry in self.carry_list:
            await self.update_carry(carry)
            sleep_for = 60 - datetime.utcnow().second
            if sleep_for < 10:
                sleep_for = 60
            await asyncio.sleep(sleep_for)

        if datetime.utcnow() > carry.when:
            if len(carry.member_list) == 0:
                channel = self.get_channel(carry.carry_id)
                await channel.send(f'<@{carry.owner}>... Sorry no one joined your carry. Please try again later!')
            else:
                notify_str = f'<@{carry.owner}>'
                for carry_member in carry.member_list:
                    notify_str += f' <@{carry_member}>'

                notify_str += ". The carry is now starting! " \
                        "Please meet up in CH16 Guild HQ. For Carrier, please ensure that you are the party owner. " \
                        "For people getting carried, please open your party -> search for the party leader -> " \
                        "apply to party. Stay fresh and have fun!"

                channel = self.get_channel(carry.carry_id)
                message = await channel.send(notify_str)

            self.carry_list.remove(carry)
            pickle_out = open("carries.pickle", "wb")
            pickle.dump(self.carry_list, pickle_out)

    async def update_carry(self, carry):
        embed_message = carry.update_embed(self)
        channel = self.get_channel(carry.carry_id)
        message = await channel.fetch_message(carry.message_id)
        await message.edit(embed = embed_message)

    async def on_raw_reaction_add(self, payload):
        user = self.get_guild(539219885922713620).get_member(payload.user_id)
        if user == None:
            print("User not found in Cache")
            user = await self.fetch_user(payload.user_id)
            if user == None:
                print("User does not exist")
                return
            print(f"{user.display_name} wasnt found in cache")
        if user.id == self.user.id:
            return

        if user.bot == True:
            return
        if payload.emoji.name == "UmbreonHappy" and payload.channel_id in self.carry_channel:
            message_id = payload.message_id
            for carry in self.carry_list:
                if carry.message_id == message_id:
                    if user.id == carry.owner:
                        channel = self.get_channel(payload.channel_id)
                        await channel.send(f"<@{user.id}> you cant react to your own carry... You're already the leader of the carry!", delete_after=30) 
                        channel = self.get_channel(payload.channel_id)
                        message = await channel.fetch_message(payload.message_id)
                        for react in message.reactions:
                            if react.emoji.name == 'UmbreonHappy':
                                await react.remove(user)
                        return
                    is_add_successful, status_code = carry.add_people(user.id)
                    if is_add_successful == True:
                        await self.update_carry(carry)
                        pickle_out = open("carries.pickle", "wb")
                        pickle.dump(self.carry_list, pickle_out)
                    elif status_code == 1:
                        channel = self.get_channel(payload.channel_id)
                        await channel.send(f"Sorry <@{user.id}>. Party is currently full. Please try again once a spot is open", delete_after=30)
                    elif status_code == 2:
                        pass


    async def on_raw_reaction_remove(self, payload):
        user = self.get_user(payload.user_id)
        if user == None:
            print("User not found in Cache")
            return

        if user.id == self.user.id:
            return

        if user.bot == True:
            return
        if payload.emoji.name == "UmbreonHappy" and payload.channel_id in self.carry_channel:
            message_id = payload.message_id
            for carry in self.carry_list:
                if carry.message_id == message_id:
                    if user.id == carry.owner:
                        return
                    is_remove_successful, status_code = carry.remove_people(user.id)
                    if is_remove_successful == True:
                        await self.update_carry(carry)
                        pickle_out = open("carries.pickle", "wb")
                        pickle.dump(self.carry_list, pickle_out)
                    elif status_code == 1 or status_code == 2: # Should never really happen... unless I misthought something
                        print("Something went terriby wrong o.o")

    async def scrap(self):
        channel = self.get_channel(738886647059316838)
        with open("birthdays.txt", "a+") as fp:
            async for message in channel.history(limit = None):
                parsed = dateparser.parse(message.content)
                if parsed == None:
                    print(f"cannot parse message {message.content} from {message.author.id}-{message.author.display_name}")
                    fp.write(f"error -- {message.author.id}-{message.author.display_name}-{message.content}\n")
                else:
                    fp.write(f"{message.author.id}-{message.author.display_name}-{message.content}\n")
                    
    async def add_birthday(self, message):
        channel = self.get_channel(738886647059316838)
        parsed = dateparser.parse(message.content)
        if parsed == None:
            print(f"cannot parse message {message.content} from {message.author.id}-{message.author.display_name}")
            await self.get_user(132996207831285760).send(f"cannot parse message {message.content} from {message.author.id}-{message.author.display_name}")
        else:
            with open("birthdays.txt", "a+") as fp:
                fp.write(f"{message.author.id}:-:{message.author.display_name}:-:{message.content}\n")
            self.birthdays = Birthdays()

client=MyClient()
client.loop.create_task(client.change_channel_name())
client.run(os.getenv('DISCORD_KEY'))
