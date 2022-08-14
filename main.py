import asyncio
from join import join_public_entity, join_private_entity
from telethon import TelegramClient, utils

clients = [
  {'API_ID': 'id', 'API_HASH': 'hash'}
]

async def main():
  link = input('Введите ссылку на канал: ')
  is_public = True if input('Если канал публичный - введите 1, иначе - 0: ') == '1' else False
  for client in clients:
    session = TelegramClient(str(clients.index(client)), api_id=client['API_ID'], api_hash=client['API_HASH'])
    await session.start()
    link = utils.parse_username(link)[0]
    try:
      if is_public:
        await join_public_entity(link, session)
      else:
        await join_private_entity(link, session)
    except BaseException as e:
      print(e)
      continue

    me = await session.get_me()
    print(f'{me.first_name} успешно вступил(а) в {link}')

if __name__ == '__main__':
  asyncio.run(main())