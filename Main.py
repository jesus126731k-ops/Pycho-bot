import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os
import asyncio

# ===== CONFIGURACIÓN =====
TOKEN = os.getenv("TOKEN")  # TU TOKEN VA EN SECRETS
LOG_CHANNEL_ID = 0  # AQUI PEGAS EL ID DEL CANAL #pycho-logs

AUTHORIZED_IDS = [
    1396327124016562217  # TU ID
]

DARK_MESSAGES = [
    "Estoy observando desde las sombras...",
    "Nada escapa a PYCHO.",
    "Tu actividad ha sido registrada.",
    "Las sombras lo vieron todo."
]

# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTO DE INICIO =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ PYCHO conectado como {bot.user}")

# ===== VERIFICADOR DE AUTORIZACIÓN =====
async def check_auth(interaction: discord.Interaction):
    if interaction.user.id not in AUTHORIZED_IDS:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if log_channel:
            await log_channel.send(
                f"🚨 **INTENTO NO AUTORIZADO**\n"
                f"Usuario: {interaction.user}\n"
                f"ID: {interaction.user.id}\n"
                f"Servidor: {interaction.guild}\n"
                f"Hora: {now}"
            )

        await interaction.response.send_message(
            "⛔ **Acceso denegado.**\n"
            "Tu intento ha sido registrado.\n"
            "Tu IP ha sido recopilada (broma).",
            ephemeral=True
        )
        return False
    return True

# ===== /CHAT =====
@bot.tree.command(name="chat", description="Hablar como PYCHO en el canal")
@app_commands.describe(mensaje="Mensaje que dirá PYCHO")
async def chat(interaction: discord.Interaction, mensaje: str):
    if not await check_auth(interaction):
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(f"🩸 **PYCHO:** {mensaje}")
    await interaction.followup.send("✅ Mensaje enviado.", ephemeral=True)

# ===== /GHOSTPING =====
@bot.tree.command(name="ghostping", description="Ping fantasma (se borra rápido)")
@app_commands.describe(usuario="Usuario a pingear")
async def ghostping(interaction: discord.Interaction, usuario: discord.Member):
    if not await check_auth(interaction):
        return

    await interaction.response.defer(ephemeral=True)

    msg = await interaction.channel.send(f"{usuario.mention}")
    await asyncio.sleep(0.3)
    await msg.delete()

    await interaction.followup.send("👻 Ping fantasma ejecutado.", ephemeral=True)

# ===== /SPAM =====
@bot.tree.command(name="spam", description="Envía 2-3 mensajes rápidos")
@app_commands.describe(mensaje="Mensaje a spamear")
async def spam(interaction: discord.Interaction, mensaje: str):
    if not await check_auth(interaction):
        return

    await interaction.response.defer(ephemeral=True)

    for _ in range(3):
        await interaction.channel.send(mensaje)
        await asyncio.sleep(0.5)

    await interaction.followup.send("✅ Spam enviado.", ephemeral=True)

# ===== /ANUNCIO =====
@bot.tree.command(name="anuncio", description="Anuncio oscuro de PYCHO")
@app_commands.describe(mensaje="Mensaje del anuncio")
async def anuncio(interaction: discord.Interaction, mensaje: str):
    if not await check_auth(interaction):
        return

    await interaction.response.defer(ephemeral=True)
    await interaction.channel.send(f"📢 **ANUNCIO DE PYCHO**\n{mensaje}")
    await interaction.followup.send("✅ Anuncio enviado.", ephemeral=True)

# ===== /SUSURRO =====
@bot.tree.command(name="susurro", description="Mensaje oscuro privado a un usuario")
@app_commands.describe(usuario="Usuario destino", mensaje="Mensaje a enviar")
async def susurro(interaction: discord.Interaction, usuario: discord.Member, mensaje: str):
    if not await check_auth(interaction):
        return

    await interaction.response.defer(ephemeral=True)

    try:
        await usuario.send(f"🩸 **PYCHO TE OBSERVA:**\n{mensaje}")
        await interaction.followup.send("✅ Susurro enviado.", ephemeral=True)
    except:
        await interaction.followup.send("❌ No pude enviar el susurro.", ephemeral=True)

# ===== /INVITAR =====
@bot.tree.command(name="invitar", description="Obtiene el link de invitación del bot")
async def invitar(interaction: discord.Interaction):
    if not await check_auth(interaction):
        return

    perms = discord.Permissions(
        send_messages=True,
        manage_messages=True,
        read_message_history=True,
        mention_everyone=True
    )

    link = discord.utils.oauth_url(bot.user.id, permissions=perms)
    await interaction.response.send_message(f"🔗 **Link de PYCHO:**\n{link}", ephemeral=True)

# ===== EJECUCIÓN =====
bot.run(TOKEN)
