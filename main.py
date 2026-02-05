import discord
from discord.ext import commands
import asyncio
import os

# Configuration
ADMIN_ID = {}
MESSAGE_FILE = "configured_message.txt"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

waiting_for_message = {}

def load_configured_message():
    """Charge le message configuré depuis le fichier"""
    try:
        if os.path.exists(MESSAGE_FILE):
            with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
    except Exception as e:
        print(f"Erreur lors du chargement du message: {e}")
    return "Aucun message configuré pour le moment."

def save_configured_message(message):
    """Sauvegarde le message configuré dans le fichier"""
    try:
        with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
            f.write(message)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

@bot.event
async def on_ready():
    print(f'{bot.user} est connecté et prêt!')
    print(f"ID du bot: {bot.user.id}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name="Lien en DM"))
    print(f"{bot.user} a changé !")
    await bot.tree.sync()
    print(f"{bot.user} a les commandes slash synchro")

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
    

    if message.author.id in waiting_for_message:
        channel = waiting_for_message[message.author.id]
        
        
        if save_configured_message(message.content):
            embed = discord.Embed(
                title="✅ Configuration réussie",
                description=f"Le message a été configuré avec succès !\n\n**Message configuré:**\n{message.content}",
                color=discord.Color.green()
            )
            embed.set_footer(text="IKZ BOT")
            await channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Une erreur s'est produite lors de la sauvegarde du message.",
                color=discord.Color.red()
            )
            embed.set_footer(text="IKZ BOT")
            await channel.send(embed=embed)
        
        
        del waiting_for_message[message.author.id]
        return
    
    
    await bot.process_commands(message)
    
    
    if isinstance(message.channel, discord.DMChannel):
        configured_message = load_configured_message()
        await message.channel.send(configured_message, suppress_embeds=False)

@bot.command(name='set')
async def set_message(ctx):
    """Commande pour configurer le message (réservée à l'admin)"""
    
    
    if ctx.author.id not in ADMIN_ID:
        embed = discord.Embed(
            title="❌ Accès refusé",
            description="Vous n'avez pas les permissions pour utiliser cette commande.",
            color=discord.Color.red()
        )
        embed.set_footer(text="IKZ BOT")
        await ctx.send(embed=embed)
        return
    
    
    embed = discord.Embed(
        title="🔧 Configuration du message",
        description="Veuillez envoyer le message que vous souhaitez configurer.",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Configuration en attente... | IKZ BOT")
    
    await ctx.send(embed=embed)
    
    
    waiting_for_message[ctx.author.id] = ctx.channel

@bot.command(name='status')
async def status(ctx):
    """Affiche le message actuellement configuré (pour l'admin)"""
    
    if ctx.author.id not in ADMIN_ID:
        embed = discord.Embed(
            title="❌ Accès refusé",
            description="Vous n'avez pas les permissions pour utiliser cette commande.",
            color=discord.Color.red()
        )
        embed.set_footer(text="IKZ BOT")
        await ctx.send(embed=embed)
        return
    
    configured_message = load_configured_message()
    
    embed = discord.Embed(
        title="📋 Message actuellement configuré",
        description=configured_message,
        color=discord.Color.blue()
    )
    embed.set_footer(text="IKZ BOT")
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.CommandNotFound):
        return  
    
    print(f"Erreur de commande: {error}")

# Lancement du bot
if __name__ == "__main__":
    print("Démarrage du bot...")
    
    # Discord bot token
    TOKEN = ""
    
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du bot: {e}")