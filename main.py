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
    global preconsent
    global pmInit
    global pmMessages
    global adv#asynchronous functions are hard
    to_send = {}

    msg = message.content
    msgch = message.channel
    msggd = message.guild

    #what was i going to do here?

    if message.author == client.user:#so it doesn't look at its own messages
        return

    if msg.startswith('!setup'):
        setupchannel = cmd.setup(setupchannel, msgch)

    elif msg.startswith('!add'):
        channels = cmd.add(msgch, channels)


    elif msg.startswith('!catadd'):
        channels = cmd.catadd(msgch, channels)

    elif msg.startswith('!servadd'):
        channels = cmd.servadd(msggd, channels)

    elif msg.startswith('!remove'):
        channels = cmd.remove(msgch, channels)

    elif msg.startswith('!catrm'):
        channels = cmd.catrm(msgch, channels)

    elif msg.startswith('!servrm'):
        channels = cmd.servrm()

    elif msg.startswith('!pmcatadd'):
        pmChannels = cmd.pmcatadd(admins, msgch, pmChannels)

    elif msg.startswith('!stcatadd'):
        stChannels = cmd.catadd(admins, msgch, stChannels)

    if msg.startswith('!admin'):
        admin_role, admins = cmd.admin(message, admin_role, admins)

    elif msg.startswith('!player'):
        player_role = cmd.player(message, player_role)

    elif msg.startswith('!stupid'):
        stupid = cmd.stupid(message, stupid)

    elif msg.startswith('!pladd'):
        players = cmd.pladd(players, message)

    elif msg.startswith('!divide'):
        day, pmMessages = cmd.divide(day, channels, adv, consent)

    elif msg.startswith('!reset'):
        day = cmd.reset(day, message)

    elif msg.startswith('!tick'):
        day = cmd.tick(day)

    elif msg.startswith('!newgame'):
        (day, playMsg, admins,
        preconsent, consent, adv) = cmd.newgame(playMsg,playerRole,admin,
                                                players,message)

    elif msg.startswith('!ping'):#easiest way to test if the bot is online
        cmd.ping(day, channels, players, admins)

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
            to_send['NO UWU'] = msgch
            if stupid:
                sinner = message.author
                if stupid not in sinner.roles:
                    await sinner.add_roles(stupid, reason='Filthy UWUer')

    for msgout in to_send:
        await to_send[msgout].send(msgout)

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
