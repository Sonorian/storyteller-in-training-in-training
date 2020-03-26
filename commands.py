import discord

class Error(Exception):
    """Base class for exceptions for this module"""
    pass

class StateError(Error):
    """Raised when a command is attempted in an incorrect state.

    Attributes:
        previous -- current state
        next -- state required
        message -- explanation of why the state was wrong
    """

    def __init__(self, state, rstate, message='Incorrect state. '
                                               'This should be depracated'):
        self.state = state
        self.rstate = rstate
        self.message = message

class ChannelError(Error):
    """Raised when a command is attempted in the wrong channel.

    Attributes:
        channel -- current channel
        rchannel -- required channel
        message -- explanation
    """

    def __init__(self, channel, rchannel, message):
        self.channel = previous
        self.rchannel = next
        self.message = message

class UseError(Error):
    """Raised when program is run independently"""
    pass

if __name__ == '__main__':
    raise UseError

def setup(setupchannel, msgch):
    to_send = {}
    """sets one channel to be used for all admin commands"""
    if not setupchannel:
        setupchannel = msgch
        to_send[('Setup channel has been set to {}. This is permanent.'
                 .format(setupchannel.mention))] = msgch
        to_send[('Please set roles with `!player @player`, '
                 '`!admin @admin1 @admin2`, `!stupid @stupid`. '
                 'Then set channels with `!add/remove`, '
                 '`!catadd/rm`, `!servadd/rm`.')] =
    else:
        try:
            await msgch.send('Setup Channel already set to {}'
                             .format(setupchannel.mention))
            raise ChannelError(msgch.name, setupchannel.name,
                              'Command not used in setup channel')
        except ChannelError:
            pass
    return setupchannel, to_send

def add(msgch, channels):
    """Adds a single channel to be divided"""
    if msgch in channels:
        await msgch.send('This channel has already been added')
    else:
        channels.append(msgch)
        await msgch.send('Added channel {}'.format(msgch.mention))
    return channels

def catadd(msgch, channels):
    """Adds a category to be divided"""
    if not msgch.category:
        await msgch.send('This channel does not appear to be '
                         'part of a category; please use `!add`')
        return channels
    cats = msgch.category.text_channels
    for ch in cats:
        if ch not in channels:
            channels.append(ch)
    await msgch.send('All channels in category `{}` have been added.'
                     .format(msgch.category.name))
    return channels

def servadd(msggd, channels):
    """Adds all channels to be divided"""
    for ch in msggd.text_channels:
        if ch not in channels:
            channels.append(ch)
    await msgch.send('All channels in server `{}` have been added.'
                     .format(msggd.name))
    return channels

def remove(msgch, channels):
    """Removes a single channel"""
    if msgch not in channels:
        await msgch.send('This channel has not been added')
        return
    channels.remove(msgch)#removes the channel from the list
    await msgch.send('Removed channel {}'.format(msgch.mention))
    return

def catrm(msgch, channels):
    """Removes a category"""
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
    return channels

def servrm():
    """Wipes the list of channels"""
    channels = []
    return channels

def pmcatadd(admins, msgch, pmChannels):
    if not admins:
        await message.channel.send('Please add admins - '
                                   '`!admin` will add all current admins,'
                                   'so remove all Storytellers in Training '
                                   'first (except me)')
    elif msgch.category:
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
    return pmChannels

def stcatadd(admins, msgch, stChannels):
    if not admins:
        await message.channel.send('Please add admins - '
                                   '`!admin` will add all current admins,'
                                   'so remove all Storytellers in Training '
                                   'first (except me)')
    elif not msgch.category:
        await msgch.send('This channel does not appear '
                         'to be part of a category')
    else:
        cats = msgch.category.text_channels
        for ch in cats:
            if ch not in stChannels:
                stChannels[ch] = []
        for ch in stChannels:
            users = [user for user in ch.members if user not in admins]
            """!!!WARNING!!! - When using this command,
            make sure to remove all storytellers in training.
            It's a pain to use this multiple times between rounds.
            """
            if len(users) > 1:
                await ch.send('Error: Incorrect number of '
                              'non-admins found, defaulting to `{}`'
                              .format(users[0].display_name))
            elif len(users) == 1:
                stChannels[ch] = [users[0], None]
        await msgch.send('`{}` set as '
                         'Storyteller-Player channels'
                         .format(msgch.category.name))
    return stChannels

def admin(message, admin, admins):
    admin = message.role_mentions
    if admin:
        await message.channel.send('Admin roles set.')
    else:
        await msgch.send('Please mention at least one role.')
    for user in message.guild.members:
        if any(role in user.roles for role in admin):
            admins.append(user)
    return admin, admins

def player(message, player):
    msgch = message.channel
    role = message.role_mentions
    if role:
        player = role[0]
        await msgch.send('Stupid role set to {}'.format(player.mention))
    else:
        await msgch.send('Please mention a role.')
    return player

def stupid(message, stupid):
    msgch = message.channel
    role = message.role_mentions
    if role:
        stupid = role[0]
        await msgch.send('Stupid role set to {}'.format(stupid.mention))
    else:
        await msgch.send('Please mention a role.')
    return stupid

def divide(day, channels, adv, consent):
    """Sends day dividers, as well as reset PM system and stupid roles"""
    if day == 0:
        div = ('————————— NEW GAME —————————')
    else:
        div = ('————————— DAY {} —————————'.format(str(day)))
    for ch in channels:#where the magic happens
        await ch.send(div)
    if adv:
        pmMessages = []
        for ch in consent:
            info = await ch.send('To initiate a PM, send a message '
                                 'with nothing but an @mention '
                                 'of the other player. '
                                 'Anything else will be deleted. '
                                 'To accept a PM, simply react '
                                 'to their message.')
            pmMessages.append(info)
            consent[ch] = ['init']
    day += 1
    if stupid:
        for player in msggd.members:
            if stupid in player.roles:
                updated = player.roles
                updated.remove(stupid)
                await player.edit(roles = updated,
                                  reason='A new day dawns, '
                                  'and all is forgiven')
        """Note: currently does not
        appear to work. Also does not
        appear to affect function.
        """
    return pmMessages

def reset(message):
    """Manually change the day"""
    clean = message.content.replace('!reset','')
    try:
        day = int(clean)
    except TypeError:
        await message.channel.send('Please use the format `!reset [number]`')
        day = 0
    await message.channel.send('The next day to be sent will be Day {}. '
                               'Please use `!divide` to send day dividers'
                               .format(str(day)))
    return day

def tick(day):
    """Manually change the day.
    Deprecated - reset can do everything now.
    """
    day += 1
    return day

def newgame(playMsg, playerRole, admin, players, message):
    """Resets day, sets admins, starts preconsent system"""
    msgch = message.channel
    adv = None
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
    preconsent = {}
    for user in players:
        await user.add_roles(playerRole, reason = 'Assigned player')
    for user in message.guild.members:
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
            consent[ch] = ['ng']#combine pre- and consent into one
    day = 0
    playMsg = None
    await msgch.send('A new game has started, '
                     'player roles have been assigned, '
                     'and the day counter has been reset. '
                     'Please use `!divide` to send new game dividers')
    return day, playMsg, admins, preconsent, consent

def ping(msgch, day, channels, players, admins):
    def txlist(ls):
        outs = ''
        for x in range(0,len(ls)):
            if x != 0:
                outs += ', '
            outs += ls[x].display_name
        return outs
    msgch.send('Ping received. Next day is {}.'
               'Sending dividers to {} channels'
               .format(str(day), str(len(channels))))
    if players:
        msgch.send('Current players are {}'.format(txlist(players)))
    if admins:
        msgch.send('Current admins are {}'.format(txlist(admins)))

def pladd(players, message):
    pls = message.mentions
    for pl in pls:
        players.append(pl)
    return players
