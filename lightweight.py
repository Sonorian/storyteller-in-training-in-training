import discord
client = discord.Client()

@client.event
async def on_message(message):
    msg = message.content
    if msg.startswith('!divide'):
        try:
            day = int(msg.replace('!divide',''))
            if day == 0:
                out = '————————— NEW GAME —————————'
            else:
                out = '————————— DAY {} —————————'.format(day)
            for ch in message.guild.text_channels:
                await ch.send(out)
        except:
            pass

client.run('key')
