# This is a simple example of a chainlit app.
from typing import Dict, Optional

from chainlit.client.base import AppUser

from chainlit import AskUserMessage, Message, oauth_callback, on_chat_start


@on_chat_start
async def main():
    res = await AskUserMessage(content="What is your name?", timeout=30).send()
    if res:
        await Message(
            content=f"Your name is: {res['content']}.\nChainlit installation is working!\nYou can now start building your own chainlit apps!",
        ).send()


@oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_app_user: AppUser,
) -> Optional[AppUser]:
    if provider_id == "pointclickcare":
        return default_app_user
    return None
