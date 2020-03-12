import socks
import configparser
from telethon import TelegramClient, events, sync
import time 


def main():
    """
    Main function
    """
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    API_ID = config['telegram']['API_ID']
    API_HASH = config['telegram']['API_HASH']
    SESSION_NAME = config['telegram']['SESSION_NAME']
    CHAT_IDS = config['saver']['CHAT_IDS']
    if CHAT_IDS:
        CHAT_IDS = set([int(x) for x in CHAT_IDS.split(',')])
    else:
        CHAT_IDS = None
    with TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=(socks.SOCKS5, 'tor', 9050)) as client:
        client.connect()
        saved_messages_dialog = [x for x in client.get_dialogs() if x.id == client.get_me().id]
        assert len(saved_messages_dialog) == 1
        saved_messages_dialog = saved_messages_dialog[0]
        @client.on(events.NewMessage)
        async def handler(event):
            if CHAT_IDS is None or event.to_id.channel_id in CHAT_IDS:
                await client.forward_messages(saved_messages_dialog, event.message)        
        client.run_until_disconnected()
    

if __name__ == "__main__":
    main()
