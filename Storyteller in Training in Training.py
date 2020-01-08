import discord#https://discordpy.readthedocs.io/en/latest/index.html
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()#c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None
stupid = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))#when this pops up in terminal you can use the bot

@client.event
async def on_message(message):#looks at every message sent in the server
    global state
    global channels
    global day
    global setupchannel
    global stupid#asynchronous functions are hard

    msg = message.content
    msgch = message.channel

    if message.author == client.user:#so it doesn't look at its own messages
        return

    if msg.startswith('!setup') and state != 'channel':
        if not setupchannel:
            setupchannel = msgch#sets one channel to be used for all admin commands
            await msgch.send('Setup channel has been set to `' + setupchannel.name + '`. This is permanent.')#if you're new to the library [channel].send('txt') sends txt in [channel]
        if setupchannel == msgch:
            state = 'channel'
            await msgch.send('Please set channels with `!add`, `!remove`, `!catadd`, `!catrm`, `!servadd`, or `!servrm`. Type `!done` when finished')
        else:
            await msgch.send('Please use `!setup` in `' + setupchannel.name + '`')
    if state == 'channel':
        if msg.startswith('!add'):
            if msgch in channels:
                await msgch.send('This channel has already been added')
            else:
                channels.append(msgch)#adds a specific channel to the list to be divided.
                await msgch.send('Added channel `' + msgch.name + '`')
        if msg.startswith('!catadd'):
                if msgch.category:#if the channel belongs to a category
                    cats = msgch.category.text_channels
                    for ch in cats:
                        if ch not in channels:
                            channels.append(ch)#adds each channel that isn't already on the list
                    await msgch.send('All channels in category `' + msgch.category.name + '` have been added.')
                else:
                    await msgch.send('This channel does not appear to be part of a category; please use `!add`')
        if msg.startswith('!servadd'):
            for ch in message.guild.text_channels:
                if ch not in channels:
                    channels.append(ch)
            await msgch.send('All channels in server `' + message.guild.name + '` have been added.')
        if msg.startswith('!remove'):
            if msgch not in channels:
                await msgch.send('This channel has not been added')
                return
            channels.remove(msgch)#removes the channel from the list
            await msgch.send('Removed channel `' + msgch.name + '`')
        if msg.startswith('!catrm'):
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch in channels:
                        channels.remove(ch)
                await msgch.send('All channels in category `' + msgch.category.name + '` have been removed.')
            else:
                await msgch.send('This channel does not appear to be part of a category; please use `!remove`')
        if msg.startswith('!servrm'):
            channels = []
            await msgch.send('All channels in server `' + message.guild.name + '` have been removed.')
        if msg.startswith('!done') and msgch == setupchannel:
            await msgch.send('Channels set. Use `!divide` to send day dividers, `!newgame` to start a new game, and `!reset [digit]` to manually set the day.')#this sometimes breaks, idk why
            state = 'dividing'
        if msg.startswith('!stupid'):
            role = msg.role_mentions
            if role:
                stupid = role[0]
            else:
                await msgch.send('Please mention a role.')
    if msgch == setupchannel:
        if msg.startswith('!divide'):
            if state != 'dividing':
                await msgch.send('Please finish setup via either `!setup` or `!done`.')
                return
            if day == 0:
                div = ('————————— NEW GAME —————————')
            else:
                div = ('————————— DAY ' + str(day) + ' —————————')#i really need to figure out how to do this more cleanly
            for chan in channels:#where the magic happens
                await chan.send(div)#puts the day divider in every channel slated to be divided
            day += 1
            if stupid:
                for player in guild.members:
                    if stupid in player.roles:
                        updated = player.roles
                        updated.remove(stupid)
                        player.edit(updated, reason='A new day dawns, and all is forgiven')
        if msg.startswith('!newgame'):
            if state != 'dividing':
                await msgch.send('Please finish setup via either `!setup` or `!done`.')
                return
            day = 0
            await msgch.send('A new game has started, and the day counter has been reset. Please use `!divide` to send new game dividers')
        if msg.startswith('!reset'):
            if state != 'dividing':
                await msgch.send('Please finish setup via either `!setup` or `!done`.')
                return
            digits = ['0','1','2','3','4','5','6','7','8','9']
            if msg[-1] not in digits:#i'm sure there's a better way to do this like with numpy or smth
                await msgch.send('Please enter a valid digit')
                return
            day = int(msg[-1])
            await msgch.send('The next day to be sent will be Day ' + str(day) + '. Please use `!divide` to send day dividers')
        if msg.startswith('!ping'):
            #chanOut = ''
            #first = 0
            #if channels:
            #    for ch in channels:
            #        if first:
            #            chanOut += ', '
            #        graved = '`' + ch.name + '`'
            #        chanOut += graved
            #        first = None
            #else:
            #    chanOut = '`None`'
            await msgch.send('Ping received.')#no longer sends list of all channels - went over max message limit
            if state == 'added':#sends a status update
                await msgch.send('Please setup via `!setup`.')
            elif state == 'channel':
                await msgch.send('Please finish setup, then type `!done`.')
            elif state == 'dividing':
                await msgch.send('Please send day dividers via `divide`.')
    if 'uwu' in msg or 'Uwu' in msg or 'UWu' in msg or 'UwU' in msg or 'uWu' in msg or 'uWU' in msg or 'uwU' in msg or 'UWU' in msg:
        await msgch.send(':BANN:***NO UWU***:dont::BANN:')#Only works in the server I use, be sure to edit this in your version
        if stupid:
            sinner = msg.author
            if stupid not in sinner.roles:
                sinner.add_roles(stupid, reason='Filthy UWUer')

client.run('insert key here')
