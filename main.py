import discord

prefix = "s!"
roleprefix = "stream-"
client = discord.Client()

debug = False #set false for normal use

if debug:
    guild_id = 297811083308171264
    owner_id = [240995021208289280]

else:
    guild_id = 144680570708951040
    owner_id = [140564059417346049]
    
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.id != 144680570708951040:
            await guild.leave()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if (not message.content.startswith(prefix)) or message.content.startswith(prefix+prefix):
        return
    
    command = message.content.split(' ')[0][len(prefix):].lower()
    
    htc = client.get_guild(guild_id)
    bot = htc.get_member(client.user.id)
    inHTC = (htc.get_member(message.author.id) != None)
    isOwner = message.author.id in owner_id
    roles = htc.roles
    teams = []

    for role in roles:
        if role.name.startswith(roleprefix):
            teams.append(role)

    if isOwner:
        if command == "permcheck":
            hasPerm = bot.guild_permissions.manage_roles
            if not hasPerm:
                print("**Alert:** The bot does not have permission to manage roles.")
            else:
                print("The bot currently has permission to manage roles.")

    if (command == "help" and (isinstance(message.channel, discord.abc.PrivateChannel) or message.guild.id == guild_id)):
        names = ['`{}{}`'.format(prefix, role.name.replace(roleprefix, '')) for role in teams]
        if len(names) > 1:
            names[-1] = 'or {}'.format(names[-1])
        await message.channel.send(
            'To add or remove a stream role, say {0}. To remove all stream roles, say `{1}remove`. To get all stream roles, use `{1}all`.'.format(', '.join(names),prefix)
        )

    try:
        if (inHTC and (isinstance(message.channel, discord.abc.PrivateChannel) or message.guild.id == guild_id)):
            user = htc.get_member(message.author.id)

            if command == "remove":
                removed = False
                for role in teams:
                    if role in user.roles:
                        removed = True
                        await user.remove_roles(role)

                sent_message = None
                if removed:  d = "All of your stream roles have successfully been removed."
                else: d = "You don't have any stream roles!"
                await message.channel.send(d)

            elif command == "all":
                for role in teams:
                    await user.add_roles(role)
                await message.channel.send("You have been added to all stream roles.")

            else:
                if command in [role.name.replace(roleprefix, '') for role in teams]:
                    team = discord.utils.get(teams,name="{}{}".format(roleprefix,command))
                    result = ""
                    if team in user.roles:
                        await user.remove_roles(team)
                        result = "removed from"
                    else:
                        await user.add_roles(team)
                        result = "added to"
                    await message.channel.send("You have been {} {}'s stream role.".format(result,team.name))

    except Exception as e:
        if debug:
            raise e
        else:
            print("[ERROR] A bot-crashing error occured somewhere in the code. Error on next line.\n{}".format(e))

client.run(open("bot-token.txt").read().split("\n")[0])
