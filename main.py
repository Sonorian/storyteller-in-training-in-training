import discord  # https://discordpy.readthedocs.io/en/latest/index.html
import logging
import commands as cmd

logging.basicConfig(level=logging.INFO)
client = discord.Client()   # c/p from above link, idk what it does

state = 'added'
channels = []
day = 0
setupchannel = None
stupid_role = None
player_role = None
admin_role = []
stupid = []
players = []
admins = []
playMsg = None
pmChannels = {}     # format: TextChannel:[User0,User1]
stChannels = {}     # format: TextChannel:[user, active]
preconsent = {}     # format: Player:{Player:given?}
consent = {}        # format: TextChannel:[state,*Reciever]
pmInit = {}         # format: TextChannel:message
pmCount = {}        # format: Player:{Target:count}
adv = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # When this pops up in terminal you can use the bot.

@client.event
async def on_message(message):
    """looks at every message sent in the server.
    If it is a function command, it is executed.
    Also logs PMs.
    """
    global state
    global channels
    global day
    global setupchannel
    global admin_role
    global stupid
    global player_role
    global players
    global admins
    global playMsg
    global pmChannels
    global stChannels
    global pmInit
    global pmCount
    global adv  # asynchronous functions are hard

    msg = message.content
    msgch = message.channel
    msggd = message.guild
    to_send = {}

    if message.author == client.user:
        return
        # Makes the bot ignore its own messages

    if msg.startswith('!setup'):
        setupchannel, to_send = cmd.setup(setupchannel, msgch)

    elif msg.startswith('!add'):
        channels, to_send = cmd.add(msgch, channels)

    elif msg.startswith('!catadd'):
        channels, to_send = cmd.catadd(msgch, channels)

    elif msg.startswith('!servadd'):
        channels, to_send = cmd.servadd(msggd, channels)

    elif msg.startswith('!remove'):
        channels, to_send = cmd.remove(msgch, channels)

    elif msg.startswith('!catrm'):
        channels, to_send = cmd.catrm(msgch, channels)

    elif msg.startswith('!servrm'):
        channels, to_send = cmd.servrm(msgch)

    elif msg.startswith('!pmadd'):
        pmChannels, to_send = cmd.pmadd(message, pmChannels)

    elif msg.startswith('!pmcatadd'):
        pmChannels, to_send = cmd.pmcatadd(admins, msgch, pmChannels)

    elif msg.startswith('!stadd'):
        stChannels, to_send = pmadd(message, stChannels)

    elif msg.startswith('!stcatadd'):
        stChannels, to_send = cmd.catadd(admins, msgch, stChannels)

    elif msg.startswith('!admin'):
        admin_role, admins, to_send = cmd.admin(message, setupchannel,
                                                admin, admins)

    elif msg.startswith('!player'):
        player_role, to_send = cmd.player(message, setupchannel, player_role)

    elif msg.startswith('!stupid'):
        stupid_role, to_send = cmd.stupid(message, setupchannel, stupid_role)

    elif msg.startswith('!pladd'):
        players = cmd.pladd(players, message)

    elif msg.startswith('!divide'):
        day, consent, to_send = cmd.divide(message, setupchannel, day,
                                           channels, adv, consent)
        for sinner in stupid:   # reset stupid roles
            updated = sinner.roles
            updated.remove(stupid_role)
            await player.edit(roles=updated, reason=
                              'A new day dawns, and all is forgiven')
        stuipd = []

    elif msg.startswith('!reset'):
        day, to_send = cmd.reset(day, message)

    elif msg.startswith('!tick'):
        day = cmd.tick(day)

    elif msg.startswith('!newgame'):
        if playMsg:
            players = []
            for emj in playMsg.reactions:
                adv_reacts.append(await reaction.users().flatten())
            players = set(adv_reacts)
            for user in players:
                await user.add_roles(playerRole, reason = 'Assigned player')
        (day, playMsg, admins,
         preconsent, consent,
         adv, to_send) = cmd.newgame(playMsg, admin_role, players, message)

    elif msg.startswith('!ping'):
        to_send = cmd.ping(msgch, day, channels, players, admins)

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
                    await warning.delete(delay=5)
                else:
                    pmInit[msgch] = msg
                    consent[msgch] = ['wait', reci]
                    await msgch.set_permissions(init, overwrite=deny)
                    await msgch.set_permissions(reci, overwrite=deny)
            if consent[msgch][0] == 'wait':
                if preconsent[reci][1] == 'given':
                    consent[msgch] = ['given']
                    await msgch.set_permissions(init, overwrite=allow)
                    await msgch.set_permissions(reci, overwrite=allow)
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
            if not to_send[msgch]:
                to_send[msgch] = []
            to_send[msgch].append('***NO UWU***')
            if stupid_role:
                sinner = message.author
                if sinner not in stupid:
                    await sinner.add_roles(stupid_role, reason='Filthy UWUer')
                    stupid.append(sinner)


    for ch in to_send:
        for ms in to_send[ch]:
            ch.send(ms)

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
