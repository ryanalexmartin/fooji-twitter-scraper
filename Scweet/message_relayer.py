import discord_bot

def relay_message_and_channel(channel_id, message):
    discord_bot.client.send_message_to_channel(channel_id, message)