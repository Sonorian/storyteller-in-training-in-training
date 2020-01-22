import discord#https://discordpy.readthedocs.io/en/latest/index.html
import logging

logging.basicConfig(level=logging.INFO)
client = discord.Client()#c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None
admin = []
stupid = None
players = []
playMsg = None
pmChannels = {}#format: TextChannel:[User0,User1]
stChannels = {}#format: TextChannel:user
preconsent = {}#format: [Player,Reciever]:[message,consentGiven]
consent = {}#format: TextChannel:[state,*Reciever]
pmInit = {}#format: TextChannel:message
pmMessages = []
adv = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))#when this pops up in terminal you can use the bot

@client.event
async def on_message(message):#looks at every message sent in the server
    global state
    global channels
    global day
    global setupchannel
    global admin
    global stupid
    global playerRole
    global players
    global playMsg
    global pmChannels
    global stChannels
    global preconsent
    global pmInit
    global pmMessages
    global adv#asynchronous functions are hard

    msg = message.content
    msgch = message.channel

    if message.author == client.user:#so it doesn't look at its own messages
        return

    if msg.startswith('!setup') and state != 'channel':
        if not setupchannel:
            setupchannel = msgch#sets one channel to be used for all admin commands
            await msgch.send('Setup channel has been set to ' + setupchannel.mention + '. This is permanent.')#if you're new to the library [channel].send('txt') sends txt in [channel]
        if setupchannel == msgch:
            state = 'channel'
            await msgch.send('Please set channels with `!add`, `!remove`, `!catadd`, `!catrm`, `!servadd`, or `!servrm`. Type `!done` when finished')
        else:
            await msgch.send('Please use `!setup` in ' + setupchannel.mention)

    if state == 'channel':
        if msg.startswith('!add'):
            if msgch in channels:
                await msgch.send('This channel has already been added')
            else:
                channels.append(msgch)#adds a specific channel to the list to be divided.
                await msgch.send('Added channel ' + msgch.mention)

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

        if msg.startswith('!pmcatadd'):
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch not in pmChannels:
                        pmChannels[ch] = []
                for ch in pmChannels:
                    users = ch.members
                    for user in users:
                        for role in admin:
                            if role in user.roles:
                                users.remove(user)
                                break
                    if len(users) != 2:
                        await ch.send('Error: Incorrect number of non-admins found')
                    pmChannels[ch] = users
                await setupchannel.send('`' + msgch.category.name + '` set as PM channels')
            else:
                await msgch.send('This channel does not appear to be part of a category')

        if msg.startswith('!stcatadd'):
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch not in stChannels:
                        stChannels[ch] = []
                for ch in stChannels:
                    users = ch.members
                    for user in users:
                        for role in admin:
                            if role in user.roles:
                                users.remove(user)
                                break
                    if len(users) > 1:
                        await ch.send('Error: Incorrect number of non-admins found, defaulting to `'+ users[0].nick +'`')
                    elif len(users) < 1:
                        await ch.send('Error: Incorrect number of non-admins found, channel will not be in use.')
                    stChannels[ch] = users[0]
                await msg.channel.send('`' + msgch.category.name + '` set as Storyteller-Player channels')

        if msg.startswith('!admin'):
            admin = message.role_mentions
            if admin:
                await msgch.send('Admin roles set.')

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
            for ch in channels:#where the magic happens
                await ch.send(div)#puts the day divider in every channel slated to be divided
            if adv:
                for ms in pmMessages:
                    await ms.delete()
                for ch in consent:
                    info = await ch.send('To initiate a PM, send a message with nothing but an @mention of the other player. Anything else will be deleted. To accept a PM, simply react to their message.')
                    pmMessages.append(info)
                    consent[ch] = [init]
            day += 1
            for ch in consent:
                consent[ch] = ['init']
            if stupid:
                for player in message.guild.members:
                    if stupid in player.roles:
                        updated = player.roles
                        updated.remove(stupid)
                        await player.edit(roles = updated, reason='A new day dawns, and all is forgiven')#Note: currently does not appear to work. also does not appear to affect function.

        if msgch in pmChannels:
            init = msg.author
            allow = discord.PermissionsOverwrite
            deny = discord.PermissionsOverwrite
            allow.send_messages = True
            deny.send_messages = False
            if pmChannels[msgch][0] == init:
                reci = pmChannels[msgch][1]
            elif pmChannels[msgch][1] == init:
                reci = pmChannels[msgch][0]
            else:
                return
            if consent[msgch][0] == 'init':
                if ' ' in msg:
                    await msg.delete()
                    warning = await msgch.send(init.mention + ', please only mention the other player.')
                    await warning.delete(delay = 5)
                elif len(msg.mentions) != 1:
                    await msg.delete()
                    warning = await msgch.send(init.mention + ', please only mention the other player.')
                    await warning.delete(delay = 5)
                elif msg.mentions[0] != reci:
                    await msg.delete()
                    warning = await msgch.send(init.mention + ', please only mention the other player.')
                    await warning.delete(delay = 5)
                else:
                    pmInit[msgch] = msg
                    consent[msgch] = ['wait', reci]
                    await msgch.set_permissions(init, overwrite = deny)
                    await msgch.set_permissions(reci, overwrite = deny)
            if consent[msgch][0] == 'wait'
                if preconsent[reci][1] == 'given':
                    consent[msgch] = ['given']
                    await msgch.set_permissions(init, overwrite = allow)
                    await msgch.set_permissions(reci, overwrite = allow)
                    await pmInit[msgch].delete()
                    pmInit[msgch] = None
                    consent[msgch] = ['given']

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

        if msg.startswith('!tick'):#provides no feedback. This is intentional, as it's a temporary fix to the limits of !reset.
            if state == dividing:
                day += 1

        if msg.startswith('!newgame'):
            adv = None
            if state != 'dividing':
                await msgch.send('Please finish setup via either `!setup` or `!done`.')
                return
            if not playMsg:
                await msgch.send('Please send a message containing `react here to play`. If advanced startup features are not desired, please use `!reset 0`')
                return
            reactions = playMsg.reactions
            if reactions:
                for emj in reactions:
                    for user in await emj.users().flatten():
                        players.append(user)
            else:
                await msgch.send('Please wait for players to react. If advanced startup features are not desired, please use `!reset 0`')
                return
            adv = 'yep'
            for user in players:
                await user.add_roles(playerRole, reason = 'Assigned player')
            for ch in stChannels:#sets
                if stChannels[ch][0] in players:
                    stChannels[ch][1] = 1
            for ch in stChannels:
                for pl in stChannels:
                    if stChannels[ch][0] != stChannels[pl][0] and stChannels[ch][0] in players and stChannels[ch][1] in players:
                        preconsent[[stChannels[ch][0],stChannels[pl][0]]] = []#makes it so only players recieve preconsent messages
                if stChannels[ch][0] in players
                        await ch.send('Please react to whoever you pre-consent to a PM with.')
                for pl in preconsent:
                    note = await ch.send(pl[1].nick)
                    preconsent[pl] = [note, None]
            for ch in pmChannels:
                if pmChannels[ch][0] in players and pmChannels[ch][1] in players:
                    consent[ch] = ['ng']
            day = 0
            playMsg = None
            await msgch.send('A new game has started, player roles have been assigned, and the day counter has been reset. Please use `!divide` to send new game dividers')

        if msg.startswith('!ping'):#easiest way to test if the bot is online
            await msgch.send('Ping received.')#no longer sends list of all channels - went over max message limit
            if state == 'added':#sends a status update
                await msgch.send('Please setup via `!setup`.')
            elif state == 'channel':
                await msgch.send('Please finish setup, then type `!done`.')
            elif state == 'dividing':
                await msgch.send('Please send day dividers via `divide`.')

    if 'react here to play' in msg.lower():
        playMsg = message
        await setupchannel.send('Advanced newgame available once players have reacted')

    banned = ['uwu', 'uωu', 'uшu','u:regional_indicator_w:u']#the emoji thing doesn't work, but whatever, it doesn't hurt
    cleanMsg = msg.lower().replace(" ","")
    for word in banned:
        if word in cleanMsg:
            await msgch.send('***NO UWU***')
            if stupid:
                sinner = message.author
                if stupid not in sinner.roles:
                    await sinner.add_roles(stupid, reason='Filthy UWUer')

async def on_reaction_add(reaction, user):
    msg = reaction.message
    msgch = msg.channel
    allow = discord.PermissionsOverwrite
    allow.send_messages = True
    for ls in preconsent:
        if msg == preconsent[ls][0]:
            preconsent[ls][1] = 'given'
    if consent[msgch][0] == 'wait'
        if msg == pmInit[msgch] and user == consent[msgch][1]:
            consent[msgch] = ['given']
            await msgch.set_permissions(pmChannels[msgch][0], overwrite = allow)
            await msgch.set_permissions(pmChannels[msgch][1], overwrite = allow)



client.run('insert key here')#don't put your key in here and commit, you big dum dum
