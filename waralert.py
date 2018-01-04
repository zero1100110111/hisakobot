import asyncio
import datetime
import time
import urllib.request, json

import discord
from discord.ext import commands

acceptableAlliances = ['Knights Templar', 'Esquire Templar']
interestAlliances = ['Knights Templar', 'Esquire Templar']

class waralert():

    def __init__(self, bot):
        self.bot = bot
        self.filter = False
        self.running = False

    @commands.command(pass_context = True)
    async def wake(self, ctx):
        if ctx.message.author.id != '250785445087150080':
            return
        if self.running:
            await self.bot.say('Hisako is already awake.')
            return
        await self.bot.say('`[ hisako awakes ]`')
        self.running = True
        await self.run(ctx.message.channel.id)

    @commands.command(pass_context = True)
    async def quiet(self, ctx):
        if ctx.message.author.id != '250785445087150080':
            return
        self.running = False
        await self.bot.say('`[ hisako closes her eyes ]`')

    @commands.command(pass_context = True)
    async def filterswitch(self, ctx):
        if ctx.message.author.id != '250785445087150080':
            await self.bot.say('Insufficient permissions: you are not Ameyuri.')
            return
        self.filter = not self.filter
        await self.bot.say('`[ filter now ' + ('ON ]`\n\nOnly wars on KT/ET will be posted.' if self.filter else 'OFF ]`\n\nAll wars will be posted.'))
        return

    async def sendwar(self, warsummary, channelid):
        if self.filter:
            if not warsummary['attackerAA'] in acceptableAlliances and not warsummary['defenderAA'] in acceptableAlliances:
                return

        # details
        # if warsummary['attackerAA'] in interestAlliances or warsummary['defenderAA'] in interestAlliances:
        if True:
            req = urllib.request.Request('https://politicsandwar.com/api/war/' + str(warsummary['warID']), headers = {'User-Agent':'Chrome'})
            with urllib.request.urlopen(req) as url:
                war = json.loads(url.read().decode())['war'][0]

            req = urllib.request.Request('https://politicsandwar.com/api/nation/id=' + str(war['aggressor_id']), headers = {'User-Agent':'Chrome'})
            with urllib.request.urlopen(req) as url:
                attacker = json.loads(url.read().decode())

            req = urllib.request.Request('https://politicsandwar.com/api/nation/id=' + str(war['defender_id']), headers = {'User-Agent':'Chrome'})
            with urllib.request.urlopen(req) as url:
                defender = json.loads(url.read().decode())

            desc = '[' + attacker['leadername'] + ' of ' + attacker['name'] + '](https://politicsandwar.com/nation/id=' + str(war['aggressor_id']) + ')'
            desc += ' attacked '
            desc += '[' + defender['leadername'] + ' of ' + defender['name'] + '](https://politicsandwar.com/nation/id=' + str(war['defender_id']) + ')'
            desc += '\n\nReason: `' + war['war_reason'] + '`'

            output = discord.Embed(description = desc, colour = discord.Colour(0x000000), timestamp = datetime.datetime.strptime(war['date'].replace('00:00', '0000'), '%Y-%m-%dT%H:%M:%S%z'))
            output.set_footer(icon_url = 'https://i.imgur.com/aQqdUgy.png')
            output.add_field(name = 'Cities', value = str(attacker['cities']) + ' on ' + str(defender['cities']))
            output.add_field(name = 'Score', value = str(attacker['score']) + ' on ' + str(defender['score']))
            output.add_field(name = 'War Policy', value = attacker['war_policy'] + ' on ' + defender['war_policy'])
            output.add_field(name = 'Attacker', value = str(len(attacker['offensivewar_ids'])) + '/5 offensive slots')
            output.add_field(name = 'Defender', value = str(len(defender['defensivewar_ids'])) + '/3 defensive slots')
            output.set_author(name = war['aggressor_alliance_name'] + ' attacked ' + war['defender_alliance_name'], url = 'https://politicsandwar.com/nation/war/timeline/war=' + str(warsummary['warID']))

        # plain
        else:
            output = discord.Embed(colour = discord.Colour(0x000000), timestamp = datetime.datetime.strptime(war['date'].replace('00:00', '0000'), '%Y-%m-%dT%H:%M:%S%z'))

        output.set_author(name = warsummary['attackerAA'] + ' attacked ' + warsummary['defenderAA'], url = 'https://politicsandwar.com/nation/war/timeline/war=' + str(warsummary['warID']))

        await self.bot.send_message(discord.Object(channelid), embed = output)

    async def run(self, channelid):
        timenow = datetime.datetime.now(datetime.timezone.utc)

        while True:
            if not self.running:
                break
            timesave = datetime.datetime.now(datetime.timezone.utc)
            req = urllib.request.Request('https://politicsandwar.com/api/wars/', headers = {'User-Agent':'Chrome'})
            with urllib.request.urlopen(req) as url:
                wars = json.loads(url.read().decode())['wars']

            timewar = datetime.datetime.strptime(wars[0]['date'].replace('00:00', '0000'), '%Y-%m-%dT%H:%M:%S%z')
            index = 0
            while timewar >= timenow:
                await self.sendwar(wars[index], channelid)
                index += 1
                timewar = datetime.datetime.strptime(wars[index]['date'].replace('00:00', '0000'), '%Y-%m-%dT%H:%M:%S%z')

            timenow = timesave
            await asyncio.sleep(60)
        return

#-----------------------------------------

def setup(bot):
    bot.add_cog(waralert(bot))

#-----------------------------------------
