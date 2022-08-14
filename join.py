from typing import Optional
from telethon import TelegramClient, functions, errors

class JoinException(Exception):
  def __init__(self, description: Optional[str] = None):
    self.description = description
    super().__init__(f'Не удалось вступить. {description or ""}')


async def join_public_entity(username: str, client: TelegramClient):
  '''
    :param username: username of public channel (t.me/username)
    :param client: client for join to channel
    :raises JoinException
  '''
  try:
    await client(functions.channels.JoinChannelRequest(await client.get_entity(username)))
  except (ValueError, TypeError, errors.UsernameInvalidError):
    raise JoinException(description=f'Юзернейм {username!r} неверный.')
  except (errors.ChannelPrivateError, errors.ChannelInvalidError):
    raise JoinException()


async def join_private_entity(invite_hash: str, client: TelegramClient):
  '''
    :param invite_hash: invite_hash of private channel (t.me/invite_hash)
    :param client: client for join to channel
    :raises JoinException
  '''
  try:
    await client(functions.messages.ImportChatInviteRequest(hash=invite_hash))
  except errors.rpcerrorlist.InviteRequestSentError:  # костыль telethon'а - игнорируем ошибку об успешной заявке
    pass
  except errors.InviteHashInvalidError:
    raise JoinException(description=f'Пригласительный код {invite_hash!r} неверный.')
  except errors.InviteHashExpiredError:
    raise JoinException(description=f'Срок действия пригласительного кода {invite_hash!r} истек.')
  except (errors.ChannelPrivateError, errors.ChannelInvalidError):
    raise JoinException()