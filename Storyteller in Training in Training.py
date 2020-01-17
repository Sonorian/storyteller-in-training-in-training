import discord#https://discordpy.readthedocs.io/en/latest/index.html
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()#c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None
stupid = None
players = []
playMsg = None
pmChannels = []#i'll implement this someday

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))#when this pops up in terminal you can use the bot

@client.event
async def on_message(message):#looks at every message sent in the server
    global state
    global channels
    global day
    global setupchannel
    global stupid
    global playerRole
    global players
    global playMsg
    global pmChannels#asynchronous functions are hard

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
            role = message.role_mentions
            if role:
                stupid = role[0]
                await msgch.send('Stupid role set to' + stupid.mention)
            else:
                await msgch.send('Please mention a role.')
        if msg.startswith('!player'):
            role = message.role_mentions
            if role:
                playerRole = role[0]
                await msgch.send('Player role set to' + playerRole.mention)
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
                for player in message.guild.members:
                    if stupid in player.roles:
                        updated = player.roles
                        updated.remove(stupid)
                        await player.edit(roles = updated, reason='A new day dawns, and all is forgiven')#Note: currently does not appear to work. also does not appear to affect function.
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
        if msg.startswith('!newgame'):
            if state != 'dividing':
                await msgch.send('Please finish setup via either `!setup` or `!done`.')
                return
            if not playMsg:
                await setupchannel.send('Please send a message containing `react here to play`. If advanced startup features are not desired, please use `!reset 0`')
                return
            reactions = playMsg.reactions
            if reactions:
                for emj in reactions:
                    for user in await emj.users().flatten():
                        players.append(user)
            for user in players:
                await user.add_roles(playerRole, reason = 'Assigned player')
            day = 0
            playMsg = None
            await msgch.send('A new game has started, player roles have been assigned, and the day counter has been reset. Please use `!divide` to send new game dividers')
        if msg.startswith('!ping'):
            await msgch.send('Ping received.')#no longer sends list of all channels - went over max message limit
            if state == 'added':#sends a status update
                await msgch.send('Please setup via `!setup`.')
            elif state == 'channel':
                await msgch.send('Please finish setup, then type `!done`.')
            elif state == 'dividing':
                await msgch.send('Please send day dividers via `divide`.')
    if 'react here to play' in msg.lower():
        playMsg = message
    banned = ['uwu', 'uωu', 'uшu','u:regional_indicator_w:u']#the emoji thing doesn't work, but whatever, it doesn't hurt
    cleanMsg = msg.lower().replace(" ","")
    for word in banned:
        if word in cleanMsg:
            await msgch.send('***NO UWU***')
            if stupid:
                sinner = message.author
                if stupid not in sinner.roles:
                    await sinner.add_roles(stupid, reason='Filthy UWUer')

client.run('insert key here')
