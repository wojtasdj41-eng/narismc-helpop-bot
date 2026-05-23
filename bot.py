import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# Konfiguracja
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = 1224111918839631972
SERVER_ID = 1224111918839631972

# Mapowanie rang LuckPerms → Role Discord
ROLE_MAP = {
    'owner': 1224113053952508056,  # Zarząd
    'owner_dev': 1224113192972849194,  # Technik/Developer
    'headadmin': 1507505726757535795,  # HeadAdmin
    'admin': 1507505909457223751,  # Administrator
    'mod': 1507506030123421746,  # Moderator
    'helper': 1507506139640889464,  # Helper
}

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot zalogowany jako {bot.user}')
    print(f'📊 Boty na {len(bot.guilds)} serwerach')
    verify_roles.start()

@bot.event
async def on_member_join(member):
    """Weryfikacja gracza gdy dołączy do serwera"""
    print(f'🔍 Nowy gracz: {member.name}')
    
    # Sprawdzenie rangi na MC (poprzez LuckPerms API)
    mc_rank = await get_minecraft_rank(member.name)
    
    if mc_rank:
        await assign_role(member, mc_rank)
        print(f'✅ {member.name} otrzymał rangę: {mc_rank}')
    else:
        # Brak rangi - kick
        try:
            await member.kick(reason="Brak rangi na serwerze Minecraft")
            print(f'🚫 {member.name} został wyrzucony - brak rangi')
        except discord.Forbidden:
            print(f'❌ Nie mogę wyrzucić {member.name}')

@tasks.loop(minutes=5)
async def verify_roles():
    """Weryfikacja rang co 5 minut"""
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return
    
    print('🔄 Weryfikacja rang...')
    
    for member in guild.members:
        if member.bot:
            continue
        
        mc_rank = await get_minecraft_rank(member.name)
        
        # Usunięcie starych ról
        for role_id in ROLE_MAP.values():
            role = guild.get_role(role_id)
            if role in member.roles:
                await member.remove_roles(role)
        
        # Dodanie nowej roli
        if mc_rank:
            await assign_role(member, mc_rank)
        else:
            # Brak rangi - kick
            try:
                await member.kick(reason="Brak rangi na serwerze Minecraft")
                print(f'🚫 {member.name} - usunięty (brak rangi)')
            except discord.Forbidden:
                pass

async def get_minecraft_rank(username):
    """Pobranie rangi gracza z LuckPerms (symulacja)"""
    # TO MUSISZ DOSTOSOWAĆ DO SWOJEGO SERWERA MC!
    # Opcje:
    # 1. API LuckPerms
    # 2. Pliki konfigu
    # 3. Database
    
    # Przykład - musisz podłączyć do swojego systemu
    try:
        # TO ZMIEŃ NA SWÓJ SYSTEM
        response = requests.get(f'http://localhost:8080/api/user/{username}')
        if response.status_code == 200:
            data = response.json()
            rank = data.get('rank', None)
            return rank
    except:
        pass
    
    return None

async def assign_role(member, rank):
    """Przydzielenie roli na podstawie rangi"""
    guild = member.guild
    role_id = ROLE_MAP.get(rank.lower())
    
    if role_id:
        role = guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                print(f'❌ Nie mogę dodać roli dla {member.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):
    """Ręczna weryfikacja - tylko admin"""
    await verify_roles()
    await ctx.send('✅ Weryfikacja rang ukończona!')

@bot.command()
@commands.has_permissions(administrator=True)
async def check_rank(ctx, username):
    """Sprawdzenie rangi gracza"""
    rank = await get_minecraft_rank(username)
    if rank:
        await ctx.send(f'📊 **{username}** ma rangę: `{rank}`')
    else:
        await ctx.send(f'❌ **{username}** nie ma rangi lub go nie znaleziono')

bot.run(TOKEN)