from modules.discord_bot import DiscordBotContainer

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    #signal(SIGINT, handler)
    discord_bot = DiscordBotContainer()
    discord_bot.start()

    

