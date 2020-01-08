import discord#https://discordpy.readthedocs.io/en/latest/index.html
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()#c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))#when this pops up in terminal you can use the bot

@client.event
async def on_message(message):#looks at every message sent in the server
    global state
    global channels
    global day
    global setupchannel#asynchronous functions are hard

    if message.author == client.user:#so it doesn't look at its own messages
        return

    if message.content.startswith('!setup') and state != 'channel':
        if not setupchannel:
            setupchannel = message.channel#sets one channel to be used for all admin commands
            await message.channel.send('Setup channel has been set to `' + setupchannel.name + '`. This is permanent.')#if you're new to the library [channel].send('msg') sends msg in [channel]
        if setupchannel == message.channel:
            state = 'channel'
            await message.channel.send('Please set channels with `!add`, `!remove`, `!catadd`, `!catrm`, `!servadd`, or `!servrm`. Type `!done` when finished')
        else:
            await message.channel.send('Please use `!setup` in `' + setupchannel.name + '`')
    if state == 'channel':
        if message.content.startswith('!add'):
            if message.channel in channels:
                await message.channel.send('This channel has already been added')
            else:
                channels.append(message.channel)#adds a specific channel to the list to be divided.
                await message.channel.send('Added channel `' + message.channel.name + '`')
        if message.content.startswith('!catadd'):
                if message.channel.category:#if the channel belongs to a category
                    cats = message.channel.category.text_channels
                    for ch in cats:
                        if ch not in channels:
                            channels.append(ch)#adds each channel that isn't already on the list
                    await message.channel.send('All channels in category `' + message.channel.category.name + '` have been added.')
                else:
                    await message.channel.send('This channel does not appear to be part of a category; please use `!add`')
        if message.content.startswith('!servadd'):
            for ch in message.guild.text_channels:
                if ch not in channels:
                    channels.append(ch)
            await message.channel.send('All channels in server `' + message.guild.name + '` have been added.')
        if message.content.startswith('!remove'):
            if message.channel not in channels:
                await message.channel.send('This channel has not been added')
                return
            channels.remove(message.channel)#removes the channel from the list
            await message.channel.send('Removed channel `' + message.channel.name + '`')
        if message.content.startswith('!catrm'):
            if message.channel.category:
                cats = message.channel.category.text_channels
                for ch in cats:
                    if ch in channels:
                        channels.remove(ch)
                await message.channel.send('All channels in category `' + message.channel.category.name + '` have been removed.')
            else:
                await message.channel.send('This channel does not appear to be part of a category; please use `!remove`')
        if message.content.startswith('!servrm'):
            channels = []
            await message.channel.send('All channels in server `' + message.guild.name + '` have been removed.')
        if message.content.startswith('!done') and message.channel == setupchannel:
            await message.channel.send('Channels set. Use `!divide` to send day dividers, `!newgame` to start a new game, and `!reset [digit]` to manually set the day.')#this sometimes breaks, idk why
            state = 'dividing'
    if message.channel == setupchannel:
        if message.content.startswith('!divide'):
            if state != 'dividing':
                await message.channel.send('Please finish setup via either `!setup` or `!done`.')
                return
            if day == 0:
                msg = ('————————— NEW GAME —————————')
            else:
                msg = ('————————— DAY ' + str(day) + ' —————————')#i really need to figure out how to do this more cleanly
            for chan in channels:#where the magic happens
                await chan.send(msg)#puts the day divider in every channel slated to be divided
            day += 1
        if message.content.startswith('!newgame'):
            if state != 'dividing':
                await message.channel.send('Please finish setup via either `!setup` or `!done`.')
                return
            day = 0
            await message.channel.send('A new game has started, and the day counter has been reset. Please use `!divide` to send new game dividers')
        if message.content.startswith('!reset'):
            if state != 'dividing':
                await message.channel.send('Please finish setup via either `!setup` or `!done`.')
                return
            digits = ['0','1','2','3','4','5','6','7','8','9']
            if message.content[-1] not in digits:#i'm sure there's a better way to do this
                await message.channel.send('Please enter a valid digit')
                return
            day = int(message.content[-1])
            await message.channel.send('The next day to be sent will be Day ' + str(day) + '. Please use `!divide` to send day dividers')
        if message.content.startswith('!ping'):
            chanOut = ''
            first = 0
            if channels:
                for ch in channels:
                    if first:
                        chanOut += ', '
                    graved = '`' + ch.name + '`'
                    chanOut += graved
                    first = None
            else:
                chanOut = '`None`'
            await message.channel.send('Ping received.')
            if state == 'added':
                await message.channel.send('Please setup via `!setup`.')
            elif state == 'channel':
                await message.channel.send('Please finish setup, then type `!done`.')
            elif state == 'dividing':
                await message.channel.send('Please send day dividers via `divide`.')

client.run('insert key here')
