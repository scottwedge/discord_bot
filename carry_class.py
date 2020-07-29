import discord
from datetime import datetime, time, timedelta
import random

class Carry():

    def __init__(self, owner, carry_id, when, message_id):
        self.owner = owner
        self.carry_id = carry_id
        self.when = when
        self.message_id = message_id
        self.member_list = []
        self.channel_role_ping_id = None
        print("Initialized")

        if self.carry_id == 547026678438690836:
            self.carry_name = "Hellux Carry"
            self.channel_role_ping_id = [736933649303339028] 
            self.image = ['https://vignette.wikia.nocookie.net/maplestory/images/b/b8/Mob_Gollux_Head.png/revision/latest?cb=20140425054234']
            self.max = 5
        elif self.carry_id == 736911310423326751:
            self.carry_name = "Lomein Carry"
            self.channel_role_ping_id = [736929465686294640]
            self.image = ['https://cdn.discordapp.com/emojis/609639640089100291.png?v=1', 'https://www.uokpl.rs/fpng/f/576-5764999_black-heaven-suu.png']
            self.max = 5
        elif self.carry_id == 539516154625130496:
            self.carry_name = "Chaos Root Abyss Carry"
            self.channel_role_ping_id = [736928629015183411] # Only have hmag role id
            self.image = ['https://cdn.wikimg.net/en/strategywiki/images/thumb/a/a4/MS_Monster_Vellum.png/300px-MS_Monster_Vellum.png'],
            self.max = 5
        elif self.carry_id == 737089087508447362:
            self.carry_name = "Hard Magnus Carry"
            self.channel_role_ping_id = [736933572891377727]
            self.image = ['https://i0.wp.com/images4.wikia.nocookie.net/__cb20120805080510/maplestory/images/d/d8/Mob_Magnus.png']
            self.max = 5
        elif self.carry_id == 539515995539111936:
            self.carry_name = "Big PP Lucid and Will Carry"
            self.channel_role_ping_id = []
            self.image = ['https://orangemushroom.files.wordpress.com/2016/08/world-selection-screen.png?w=600']
            self.max = 5
        elif self.carry_id == 736392255421546517:
            self.carry_name = "Testing Carry"
            self.channel_role_ping_id = [687416417368145930]
            self.image = ['https://cdn.discordapp.com/emojis/609639640089100291.png?v=1', 'https://www.pngjoy.com/pngm/342/6391790_maplestory-maplestory-damien-transparent-png.png', 'https://www.uokpl.rs/fpng/f/576-5764999_black-heaven-suu.png']
            self.max = 5
        else:
            print("Create Message Embed Happened to a non-bossing channel")
            exit(1)



    def add_people(self, user_id):
        if len(self.member_list) + 1 > self.max:
            return False, 1 # 1 indicates that it is currently full

        if user_id in self.member_list:
            return False, 2 # 2 indicates that user is already in the list

        self.member_list.append(user_id)
        return True, 0

    def remove_people(self, user_id):
        if len(self.member_list) - 1 < 0:
            return False, 1 # Something went wrong... should never happen
        
        if user_id not in self.member_list:
            return False, 2 # User is not in the list... should never happen

        self.member_list.remove(user_id)
        return True, 0
        
    def update_embed(self, client): 
        emotes = ['<:pepega:703359475586957393>', '<:BunnyWave:626468580531372042>', '<:Pew:609639022154874887>', '<:monkaHmmm:703359475431636992>', '<:WooLucidKitty:733081496809766963>'] 
        carry_name = self.carry_name
        owner_discord_name = client.get_guild(539219885922713620).get_member(self.owner).display_name
        embed = discord.Embed(title=carry_name, description=f"{owner_discord_name}'s {carry_name} will start in about {self.format_time(self.when - datetime.utcnow())}", color=0xFF0000)
        embed.add_field(name="<:PandaLove:618915050723344404> Carrier", value = f"{owner_discord_name}", inline=False)
        for member in self.member_list:
            member = client.get_guild(539219885922713620).get_member(member).display_name
            embed.add_field(name=f"{random.choice(emotes)} Member", value =f"{member}", inline=False)

        embed.add_field(name="How To Apply", value = "React with <:UmbreonHappy:630381177076711425>", inline=False)
        embed.add_field(name="How to Remove", value = "Remove the React :D", inline=False)
        embed.add_field(name="How to Cancel (For Carrier)", value = "type >cancel_carry", inline=False)
        embed.set_footer(text="For any bugs, please report to Snooted. Happy Bossing!")
        embed.set_thumbnail(url = f"{random.choice(self.image)}")
        return embed

    def format_time(self, time):
        #print(time)
        time_str = str(time)
        hour = time_str.split(":")[0]
        minute = time_str.split(":")[1]
        seconds = time_str.split(":")[2][0:2]
        return f"{hour} hour(s), {minute} minute(s), and {seconds} second(s)"
