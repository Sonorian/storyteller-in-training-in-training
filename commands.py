"""Insert docstring here"""
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
    """Raised when module is run independently"""
    pass

if __name__ == '__main__':
    raise UseError

def setup(setupchannel, msgch, to_send={}):
    """sets one channel to be used for all admin commands"""
    if not setupchannel:
        setupchannel = msgch
        to_send[msgch] = ['Setup channel has been set to {}. '
                          'This is permanent.'
                          .format(setupchannel.mention)]
        to_send[msgch].append('Please set roles with `!player @player`, '
                              '`!admin @admin1 @admin2`, `!stupid @stupid`. '
                              'Then set channels with `!add/remove`, '
                              '`!catadd/rm`, `!servadd/rm`.')
    else:
        to_send[msgch] = ['Setup Channel already set to {}'
                          .format(setupchannel.mention)]
    return setupchannel, to_send

def add(msgch, channels, to_send={}):
    """Adds a single channel to be divided"""
    if msgch in channels:
        to_send[msgch] = ['This channel has already been added']
    else:
        channels.append(msgch)
        to_send[msgch] = ['Added channel {}'.format(msgch.mention)]
    return channels, to_send

def catadd(msgch, channels, to_send={}):
    """Adds a category to be divided"""
    if not msgch.category:
        to_send[msgch] = ['This channel does not appear to be '
                          'part of a category; please use `!add`']
        return channels, to_send
    cats = msgch.category.text_channels
    for ch in cats:
        if ch not in channels:
            channels.append(ch)
    to_send[msgch] = ['All channels in category `{}` have been added.'
                      .format(msgch.category.name)]
    return channels, to_send

def servadd(msggd, channels, to_send={}):
    """Adds all channels to be divided"""
    for ch in msggd.text_channels:
        if ch not in channels:
            channels.append(ch)
    to_send[msgch] = ['All channels in server `{}` have been added.'
                      .format(msggd.name)]
    return channels, to_send

def remove(msgch, channels, to_send={}):
    """Removes a single channel"""
    if msgch not in channels:
        to_send[msgch] = ['This channel has not been added']
        return
    channels.remove(msgch)#removes the channel from the list
    to_send[msgch] = ['Removed channel {}'.format(msgch.mention)]
    return channels, to_send

def catrm(msgch, channels, to_send={}):
    """Removes a category"""
    if msgch.category:
        cats = msgch.category.text_channels
        for ch in cats:
            if ch in channels:
                channels.remove(ch)
        to_send[msgch] = ['All channels in category `{}` have been removed.'
                          .format(msgch.category.name)]
    else:
        to_send[msgch] = ['This channel does not appear to be '
                          'part of a category; please use `!remove`']
    return channels, to_send

def servrm(msgch, to_send={}):
    """Wipes the list of channels"""
    to_send[msgch] = 'All channels removed.'
    channels = []
    return channels, to_send

def pmadd(message, pmChannels, to_send={}):
    """Manually adds a private message channel"""
    pl = message.role_mentions
    msgch = message.channel
    if len(pl) != 2:
        to_send[msgch] = ['Error: Incorrect number of players mentioned']
    else:
        pmChannels[msgch] = [pl[0], pl[1]]
        to_send[msgch] = ['{} set as PM channel for {} and {}'
                          .format(msgch.mention, pl[0].mention, pl[1].mention)]
    return pmChannels, to_send

def pmcatadd(admins, msgch, pmChannels, to_send={}):
    """Adds private message (PM) channels from a category.

    Arguments:
    admins      [discord.Member]
                    List of players with admin role(s).
    msgch       discord.TextChannel
                    The channel the command was used in.
    pmChannels  {discord.TextChannel:[discord.Member, discord.Member]}
                    List of PM channels.
    to_send     {discord.TextChannel:['']}
                    Dict of channels and msgs to be sent. (Default {})

    Returns:
    pmChannels (updated with all channels in msgch's category)
    to_send (likewise updated)
    """
    if not admins:
        to_send[msgch] = ['Please add admins - '
                          '`!admin` will add all current admins,'
                          'so remove all Storytellers in Training '
                          'first (except me)']
    elif not msgch.category:
        to_send[msgch] = ['This channel does not appear '
                          'to be part of a category']
    else:
        cats = msgch.category.text_channels
        for ch in cats:
            if ch not in pmChannels:
                pmChannels[ch] = []
        for ch in pmChannels:
            users = [user for user in ch.members if user not in admins]
            if len(users) != 2:
                to_send[ch] = ['Error: Incorrect number of non-admins found']
                continue
            else:
                to_send[ch] = ['Set PM channel for {} and {}'
                               .format(users[0].display_name,
                               users[1].display_name)]
                pmChannels[ch] = [users, None, 'setup']
        to_send[msgch] = ['`{}` set as PM channels'
                          .format(msgch.category.name)]
    return pmChannels, to_send

def stadd(message, stChannels, to_send={}):
    """Manually adds a Storyteller-Player channel"""
    pl = message.role_mentions
    msgch = message.channel
    if len(pl) != 1:
        to_send[msgch] = ['Error: Incorrect number of players mentioned']
    else:
        pmChannels[msgch] = [pl[0], None]
        to_send[msgch] = ['{} set as ST channel for {}'
                          .format(msgch.mention, pl[0].mention)]
    return stChannels, to_send

def stcatadd(admins, msgch, stChannels, to_send={}):
    """Adds Storyteller-Player (ST) channels from a category.

    Arguments:
    admins      [discord.Member]
                    List of players with admin role(s).
    msgch       discord.TextChannel
                    The channel the command was used in.
    stChannels  {discord.TextChannel:[discord.Member, int]}
                    List of ST channels.
    to_send     {discord.TextChannel:[str]}
                    Dict of channels and msgs to be sent. (Default {})

    Returns:
    stChannels (updated with all channels in msgch's category)
    to_send (likewise updated)
    """
    if not admins:
        to_send[msgch] = ['Please add admins - '
                          '`!admin` will add all current admins,'
                          'so remove all Storytellers in Training '
                          'first (except me)']
    elif not msgch.category:
        to_send[msgch] = ['This channel does not appear '
                          'to be part of a category']
    else:
        cats = msgch.category.text_channels
        for ch in cats:
            if ch not in stChannels:
                stChannels[ch] = []
        for ch in stChannels:
            users = [user for user in ch.members if user not in admins]
            pls = len(users)
            if pls < 1:
                to_send[ch] = ['Error: No non-admins found.']
                continue
            elif len(users) > 1:
                to_send[ch] = ['Error: Incorrect number of non-admins found, '
                               'defaulting to `{}`'
                               .format(users[0].display_name)]
            stChannels[ch] = [users[0], None]
        to_send[msgch] = ['`{}` set as '
                          'Storyteller-Player channels'
                          .format(msgch.category.name)]
    return stChannels, to_send

def admin(message, setupchannel, admin, admins, to_send={}):
    """Sets admin roles and finds those members"""
    admin = message.role_mentions
    msgch = message.channel
    if msgch != setupchannel:
        pass
    elif not admin:
        to_send[msgch] = ['Please mention at least one role.']
    else:
        to_send[msgch] = ['Admin roles set.']
        for user in message.guild.members:
            if any(role in user.roles for role in admin):
                admins.append(user)
    return admin, admins, to_send

def player(message, setupchannel, player, to_send={}):
    """Sets player role"""
    msgch = message.channel
    role = message.role_mentions
    if msgch != setupchannel:
        pass
    elif not role:
        to_send[msgch] = ['Please mention a role.']
    else:
        player = role[0]
        to_send[msgch] = ['Player role set to {}'.format(player.mention)]
    return player, to_send

def stupid(message, setupchannel, stupid, to_send={}):
    """Sets stupid role"""
    msgch = message.channel
    role = message.role_mentions
    if msgch != setupchannel:
        pass
    elif not role:
        to_send[msgch] = ['Please mention a role.']
    else:
        stupid = role[0]
        to_send[msgch] = ['Stupid role set to {}'.format(stupid.mention)]
    return stupid, to_send

def divide(message, setupchannel, day, channels, adv, consent, to_send={}):
    """Sends day dividers, as well as reset PM system and stupid roles"""
    msgch = message.channel
    if msgch == setupchannel:
        if day == 0:
            div = '————————— NEW GAME —————————'
        else:
            div = '————————— DAY {} —————————'.format(day)
        for ch in channels:     # currently the only functional part
            to_send[ch] = [div]
        day += 1
        if adv:
            for ch in consent:
                to_send[ch] = ('To initiate a PM, send a message '
                               'with nothing but an @mention '
                               'of the other player.\n'
                               'Anything else will be deleted.\n'
                               'To accept a PM, simply react '
                               'to their message.')
                consent[ch] = ['init']
    return day, consent, to_send

def reset(day, message, to_send={}):
    """Manually change the day"""
    msgch = message.channel
    to_send[msgch] = []
    clean = message.content.replace('!reset','')
    try:
        day = int(clean)
    except TypeError:
        to_send[msgch].append('Please use the format `!reset [number]`')
    to_send[msgch].append('The next day to be sent will be Day {}. '
                          'Please use `!divide` to send day dividers'
                          .format(day))
    return day, to_send

def tick(day):
    """Manually increment the day.
    Deprecated - reset can do everything now.
    """
    day += 1
    return day

def newgame(playMsg, admin, players, message, adv=False, to_send={}):
    """Resets day, sets admins, starts preconsent system"""
    msgch = message.channel
    if not playMsg:
        to_send[msgch] = ['Please send a message containing '
                          '`react here to play`. '
                          'If advanced startup features are not desired, '
                          'please use `!reset 0`']
    elif not playMsg.reactions:
        to_send[msgch] = ['Please wait for players to react. '
                          'If advanced startup features are '
                          'not desired, please use `!reset 0`']
    else:
        adv = True
        for user in message.guild.members:
            admins = []
            if any(role in user.roles for role in admin):
                admins.append(user)
        for ch in stChannels:
            if not stChannels[ch]:
                continue
            if stChannels[ch][0] in players:
                stChannels[ch][1] = 1
        preconsent = {}
        for ch in stChannels:
            if not stChannels[ch]:
                continue
            ch0 = stChannels[ch][0]
            if ch0 in players:
                preconsent[ch0] = {}
                for pl in stChannels:
                    if not stChannels[pl]:
                        continue
                    pl0 = stChannels[pl][0]
                    if ch0 != pl0 and pl0 in players:
                        preconsent[ch0][pl0.display_name] = None
                to_send[ch] = ['Please react to whoever '
                               'you pre-consent to a PM with.']
                to_send[ch].append(pl0.display_name)
                # member = discord.utils.get(message.guild.members, name='Foo')
        for ch in pmChannels:
            if not pmChannels[ch]:
                continue
            if (pmChannels[ch][0] in players
                    and pmChannels[ch][1] in players):
                consent[ch] = ['new game']
    day = 0
    playMsg = None
    to_send[msgch] = ['A new game has started, '
                      'player roles have been assigned, '
                      'and the day counter has been reset.\n'
                      'Please use `!divide` to send new game dividers']
    return day, playMsg, admins, preconsent, consent, adv, to_send

def ping(msgch, day, channels, players, admins, to_send={}):
    def txlist(ls):
        outs = ''
        for x in range(0,len(ls)):
            if x != 0:
                outs += ', '
            outs += ls[x].display_name
        return outs
    to_send[msgch] = ['Ping received. Next day is {}.'
                      'Sending dividers to {} channels'
                      .format(day, len(channels))]
    if players:
        to_send[msgch].append('Current players are {}'.format(txlist(players)))
    if admins:
        to_send[msgch].append('Current admins are {}'.format(txlist(admins)))
    return to_send

def pladd(players, message):
    pls = message.mentions
    for pl in pls:
        players.append(pl)
    return players
