import discord#https://discordpy.readthedocs.io/en/latest/index.html
import logging
import commands as cmd

logging.basicConfig(level=logging.INFO)
client = discord.Client()#c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None
admin = []
stupid = None
players = []
admins = []
playMsg = None
pmChannels = {}#format: TextChannel:[User0,User1]
stChannels = {}#format: TextChannel:[user, active]
preconsent = {}#format: Player:{Reciever:[message,consentGiven]}
consent = {}#format: TextChannel:[state,*Reciever]
pmInit = {}#format: TextChannel:message
pmMessages = []
adv = None

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    #when this pops up in terminal you can use the bot

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
    global admins
    global playMsg
    global pmChannels
    global stChannels
    global preconsent
    global pmInit
    global pmMessages
    global adv#asynchronous functions are hard

    msg = message.content
    msgch = message.channel
    msggd = message.guild
    #what was i going to do here?

    if message.author == client.user:#so it doesn't look at its own messages
        return

    if msg.startswith('!setup') and state != 'channel':
        if not setupchannel:#sets one channel to be used for all admin commands
            setupchannel = msgch
            await msgch.send('Setup channel has been set to {}. '
                             'This is permanent.'.format(setupchannel.mention))
        if setupchannel == msgch:
            state = 'channel'
            await msgch.send('Please set roles with `!player @player`, '
                             '`!admin @admin1 @admin2`, '
                             '`!stupid @stupid`. '
                             'Then set channels with `!add/remove`, '
                             '`!catadd/rm`, `!servadd/rm`. '
                             'Type `!done` when finished.')
        else:
            await msgch.send('Please use `!setup` in {}'
                             .format(setupchannel.mention))

    if state == 'channel':
        #all channel-adding/removing functions
        if msg.startswith('!add'):
            if msgch in channels:
                await msgch.send('This channel has already been added')
            else:
                channels.append(msgch)
                await msgch.send('Added channel {}'.format(msgch.mention))

        if msg.startswith('!catadd'):
                if msgch.category:
                    cats = msgch.category.text_channels
                    for ch in cats:
                        if ch not in channels:
                            channels.append(ch)
                    await msgch.send('All channels in category `{}` '
                                     'have been added.'
                                     .format(msgch.category.name))
                else:
                    await msgch.send('This channel does not appear to be '
                                     'part of a category; please use `!add`')

        if msg.startswith('!servadd'):
            for ch in msggd.text_channels:
                if ch not in channels:
                    channels.append(ch)
            await msgch.send('All channels in server `{}` have been added.'
                             .format(msggd.name))

        if msg.startswith('!remove'):
            if msgch not in channels:
                await msgch.send('This channel has not been added')
                return
            channels.remove(msgch)#removes the channel from the list
            await msgch.send('Removed channel {}'.format(msgch.mention))

        if msg.startswith('!catrm'):
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch in channels:
                        channels.remove(ch)
                await msgch.send('All channels in category `{}` '
                                 'have been removed.'
                                 .format(msgch.category.name))
            else:
                await msgch.send('This channel does not appear to be '
                                 'part of a category; please use `!remove`')

        if msg.startswith('!servrm'):
            channels = []
            await msgch.send('All channels in server `{}` have been removed.'
                             .format(msggd.name))

        if msg.startswith('!done') and msgch == setupchannel:
            await msgch.send('Channels set. '
                             'Use `!divide` to send day dividers, '
                             '`!newgame` to start a new game, and '
                             '`!reset [number]` to manually set the day.')
            state = 'dividing'

        if msg.startswith('!pmcatadd'):
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch not in pmChannels:
                        pmChannels[ch] = []
                for ch in pmChannels:
                    users = [user for user in ch.members if user not in admins]
                    if len(users) != 2:
                        await ch.send('Error: Incorrect number '
                                      'of non-admins found in {}'
                                      .format(ch.mention))
                    else:
                        await msgch.send('PM channel for {} and {}'
                                     .format(users[0].display_name,
                                     users[1].display_name))
                        pmChannels[ch] = [users, None, 'setup']
                await setupchannel.send('`{}` set as PM channels'
                                        .format(msgch.category.name))
            else:
                await msgch.send('This channel does not appear '
                                 'to be part of a category')

        if msg.startswith('!stcatadd'):
            if not admins:
                await message.channel.send('Please add admins - '
                                           '`!admin` will add all current '
                                           'admins, so remove all '
                                           'Storytellers in Training first '
                                           '(except me)')
                return
            if msgch.category:
                cats = msgch.category.text_channels
                for ch in cats:
                    if ch not in stChannels:
                        stChannels[ch] = []
                for ch in stChannels:
                    users = [user for user in ch.members if user not in admins]
                        #!!!WARNING!!! - When using this command,
                        #make sure to remove all storytellers in training.
                    if len(users) > 1:
                        await ch.send('Error: Incorrect number of '
                                      'non-admins found, defaulting to `{}`'
                                      .format(users[0].display_name))
                    elif len(users) == 1:
                        stChannels[ch] = [users[0], None]

                await msgch.send('`{}` set as '
                                 'Storyteller-Player channels'
                                 .format(msgch.category.name))

        if msg.startswith('!admin'):
            admin = message.role_mentions
            if admin:
                await msgch.send('Admin roles set.')
            for user in msggd.members:
                if any(role in user.roles for role in admin):
                    admins.append(user)

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

        if msg.startswith('!pladd'):
            pls = message.mentions
            for pl in pls:
                players.append(pl)

    if msgch == setupchannel:
        if msg.startswith('!divide'):
            if state != 'dividing':
                await msgch.send('Please finish setup via either '
                                 '`!setup` or `!done`.')
                return
            if day == 0:
                div = ('————————— NEW GAME —————————')
            else:
                div = ('————————— DAY {} —————————'.format(str(day)))
            for ch in channels:#where the magic happens
                await ch.send(div)
            if adv:
                for ms in pmMessages:
                    await ms.delete()
                for ch in consent:
                    info = await ch.send('To initiate a PM, send a message '
                                         'with nothing but an @mention '
                                         'of the other player. '
                                         'Anything else will be deleted. '
                                         'To accept a PM, simply react '
                                         'to their message.')
                    pmMessages.append(info)
                    consent[ch] = [init]
            day += 1
            for ch in consent:
                consent[ch] = ['init']
            if stupid:
                for player in msggd.members:
                    if stupid in player.roles:
                        updated = player.roles
                        updated.remove(stupid)
                        await player.edit(roles = updated,
                                          reason='A new day dawns, '
                                          'and all is forgiven')
                                          #Note: currently does not
                                          #appear to work. Also does not
                                          #appear to affect function.

        if msg.startswith('!reset'):
            if state != 'dividing':
                await msgch.send('Please finish setup via '
                                 'either `!setup` or `!done`.')
                return
            clean = msg.replace('!reset','')
            day = int(clean)
            await msgch.send('The next day to be sent will be Day {}. '
                             'Please use `!divide` to send day dividers'
                             .format(str(day)))

        if msg.startswith('!tick'):
            #provides no feedback. This is intentional,
            #as it's a temporary fix to the limits of !reset.'
            if state == dividing:
                day += 1

        if msg.startswith('!newgame'):
            adv = None
            if state != 'dividing':
                await msgch.send('Please finish setup via '
                                 'either `!setup` or `!done`.')
                return
            if not playMsg:
                await msgch.send('Please send a message containing '
                                 '`react here to play`. If advanced '
                                 'startup features are not desired, '
                                 'please use `!reset 0`')
                return
            reactions = playMsg.reactions
            if reactions:
                for emj in reactions:
                    for user in await emj.users().flatten():
                        players.append(user)
            else:
                await msgch.send('Please wait for players to react. '
                                 'If advanced startup features are '
                                 'not desired, please use `!reset 0`')
                return
            adv = 'yep'
            for user in players:
                await user.add_roles(playerRole, reason = 'Assigned player')
            for user in msggd.members:
                admins = []
                if any(role in user.roles for role in admin):
                    admins.append(user)
            for ch in stChannels:
                if not stChannels[ch]:
                    continue
                if stChannels[ch][0] in players:
                    stChannels[ch][1] = 1
            for ch in stChannels:
                if not stChannels[ch]:
                    continue
                ch0 = stChannels[ch][0]
                if ch0 in players:
                    for pl in stChannels:
                        if not stChannels[pl]:
                            continue
                        pl0 = stChannels[pl][0]
                        if ch0 != pl0 and pl0 in players:
                            preconsent[ch0] = {}
                            preconsent[ch0][pl0] = []
                    await ch.send('Please react to whoever '
                                  'you pre-consent to a PM with.')
                    for pl in preconsent[ch0]:
                        note = await ch.send(pl.display_name)
                        preconsent[ch][pl] = [note, None]
            for ch in pmChannels:
                if not pmChannels[ch]:
                    continue
                if (pmChannels[ch][0] in players
                        and pmChannels[ch][1] in players):
                    consent[ch] = ['ng']
            day = 0
            playMsg = None
            await msgch.send('A new game has started, '
                             'player roles have been assigned, '
                             'and the day counter has been reset. '
                             'Please use `!divide` to send new game dividers')

        if msg.startswith('!ping'):#easiest way to test if the bot is online
            await msgch.send('Ping received.')
            if state == 'added':
                await msgch.send('Please setup via `!setup`.')
            elif state == 'channel':
                await msgch.send('Please finish setup, then type `!done`.')
            elif state == 'dividing':
                await msgch.send('Please send day dividers via `divide`.')

    if 'react here to play' in msg.lower():
        playMsg = message
        await setupchannel.send('Advanced newgame available '
                                'once players have reacted')

    if adv and pmChannels:
        if msgch in pmChannels:#what the actual fuck was this supposed to be
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
                if (' ' in msg
                        or len(message.mentions !=1
                        or message.mentions[0] != reci)):
                    await msg.delete()
                    warning = await msgch.send('{}, please only mention '
                                               'the other player.'
                                               .format(init.mention))
                    await warning.delete(delay = 5)
                else:
                    pmInit[msgch] = msg
                    consent[msgch] = ['wait', reci]
                    await msgch.set_permissions(init, overwrite = deny)
                    await msgch.set_permissions(reci, overwrite = deny)
            if consent[msgch][0] == 'wait':
                if preconsent[reci][1] == 'given':
                    consent[msgch] = ['given']
                    await msgch.set_permissions(init, overwrite = allow)
                    await msgch.set_permissions(reci, overwrite = allow)
                    await pmInit[msgch].delete()
                    pmInit[msgch] = None
                    consent[msgch] = ['given']

    banned = ['uwu', 'uωu', 'uшu']
    delim = [' ','.',',','-','_','+','|','/']
    clean_msg = msg.lower()
    for char in delim:
        clean_msg = clean_msg.replace(char,'')
    for word in banned:
        if word in clean_msg:
            await msgch.send('***NO UWU***')
            if stupid:
                sinner = message.author
                if stupid not in sinner.roles:
                    await sinner.add_roles(stupid, reason='Filthy UWUer')

async def on_reaction_add(reaction, user):
    #currently does nothing
    message = reaction.message
    msg = message.content
    msgch = message.channel
    allow = discord.PermissionsOverwrite
    deny = discord.PermissionsOverwrite
    allow.send_messages = True
    deny.send_messages = False
    for ls in preconsent:
        if message == preconsent[ls][0]:
            preconsent[ls][1] = 'given'
    if consent[msgch]:
        if consent[msgch][0] == 'wait':
            if message == pmInit[msgch] and user == consent[msgch][1]:
                consent[msgch] = ['given']
                await msgch.set_permissions(pmChannels[msgch][0],
                                            overwrite = allow)
                await msgch.set_permissions(pmChannels[msgch][1],
                                            overwrite = allow)



client.run('insert key here')#don't put your key in here and commit, dumbass
