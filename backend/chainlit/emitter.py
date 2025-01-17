import uuid
from typing import Any, Dict, cast

from chainlit.client.base import MessageDict
from chainlit.data import chainlit_client
from chainlit.message import Message
from chainlit.session import BaseSession, WebsocketSession
from chainlit.types import AskSpec, FileSpec
from socketio.exceptions import TimeoutError


class BaseChainlitEmitter:
    """
    Chainlit Emitter Stub class. This class is used for testing purposes.
    It stubs the ChainlitEmitter class and does nothing on function calls.
    """

    session: BaseSession

    def __init__(self, session: BaseSession) -> None:
        """Initialize with the user session."""
        self.session = session

    async def emit(self, event: str, data: Any):
        """Stub method to get the 'emit' property from the session."""
        pass

    async def ask_user(self):
        """Stub method to get the 'ask_user' property from the session."""
        pass

    async def send_message(self, msg_dict: dict):
        """Stub method to send a message to the UI."""
        pass

    async def update_message(self, msg_dict: dict):
        """Stub method to update a message in the UI."""
        pass

    async def delete_message(self, msg_dict: dict):
        """Stub method to delete a message in the UI."""
        pass

    async def send_ask_timeout(self):
        """Stub method to send a prompt timeout message to the UI."""
        pass

    async def clear_ask(self):
        """Stub method to clear the prompt from the UI."""
        pass

    async def enable_file_upload(self, spec):
        """Stub method to enable uploading file in the UI."""
        pass

    async def init_conversation(self, msg_dict: MessageDict):
        """Signal the UI that a new conversation (with a user message) exists"""
        pass

    async def process_user_message(self, message_dict) -> None:
        """Stub method to process user message."""
        pass

    async def send_ask_user(self, msg_dict: dict, spec, raise_on_timeout=False):
        """Stub method to send a prompt to the UI and wait for a response."""
        pass

    async def update_token_count(self, count: int):
        """Stub method to update the token count for the UI."""
        pass

    async def task_start(self):
        """Stub method to send a task start signal to the UI."""
        pass

    async def task_end(self):
        """Stub method to send a task end signal to the UI."""
        pass

    async def stream_start(self, msg_dict: dict):
        """Stub method to send a stream start signal to the UI."""
        pass

    async def send_token(self, id: str, token: str, is_sequence=False):
        """Stub method to send a message token to the UI."""
        pass

    async def set_chat_settings(self, settings: dict):
        """Stub method to set chat settings."""
        pass


class ChainlitEmitter(BaseChainlitEmitter):
    """
    Chainlit Emitter class. The Emitter is not directly exposed to the developer.
    Instead, the developer interacts with the Emitter through the methods and classes exposed in the __init__ file.
    """

    session: WebsocketSession

    def __init__(self, session: WebsocketSession) -> None:
        """Initialize with the user session."""
        self.session = session

    def _get_session_property(self, property_name: str, raise_error=True):
        """Helper method to get a property from the session."""
        if not hasattr(self, "session") or not hasattr(self.session, property_name):
            if raise_error:
                raise ValueError(f"Session does not have property '{property_name}'")
            else:
                return None
        return getattr(self.session, property_name)

    @property
    def emit(self):
        """Get the 'emit' property from the session."""

        return self._get_session_property("emit")

    @property
    def ask_user(self):
        """Get the 'ask_user' property from the session."""
        return self._get_session_property("ask_user")

    def send_message(self, msg_dict: Dict):
        """Send a message to the UI."""
        return self.emit("new_message", msg_dict)

    def update_message(self, msg_dict: Dict):
        """Update a message in the UI."""

        return self.emit("update_message", msg_dict)

    def delete_message(self, msg_dict):
        """Delete a message in the UI."""

        return self.emit("delete_message", msg_dict)

    def send_ask_timeout(self):
        """Send a prompt timeout message to the UI."""

        return self.emit("ask_timeout", {})

    def clear_ask(self):
        """Clear the prompt from the UI."""

        return self.emit("clear_ask", {})

    def enable_file_upload(self, spec: FileSpec):
        """Enable uploading file in the UI."""

        return self.emit("enable_file_upload", spec.to_dict())

    def init_conversation(self, message: MessageDict):
        """Signal the UI that a new conversation (with a user message) exists"""

        return self.emit("init_conversation", message)

    async def process_user_message(self, message_dict: MessageDict):
        # Temporary UUID generated by the frontend should use v4
        assert uuid.UUID(message_dict["id"]).version == 4

        if chainlit_client:
            message_dict["conversationId"] = await self.session.get_conversation_id()
            # We have to update the UI with the actual DB ID
            ui_message_update = cast(Dict, message_dict.copy())
            persisted_id = await chainlit_client.create_message(message_dict)
            if persisted_id:
                message_dict["id"] = persisted_id
                ui_message_update["newId"] = message_dict["id"]
                await self.update_message(ui_message_update)

        if not self.session.has_user_message:
            self.session.has_user_message = True
            await self.init_conversation(message_dict)

        message = Message.from_dict(message_dict)
        self.session.root_message = message

    async def send_ask_user(
        self, msg_dict: Dict, spec: AskSpec, raise_on_timeout=False
    ):
        """Send a prompt to the UI and wait for a response."""

        try:
            # Send the prompt to the UI
            res = await self.ask_user(
                {"msg": msg_dict, "spec": spec.to_dict()}, spec.timeout
            )

            # End the task temporarily so that the User can answer the prompt
            await self.task_end()

            if chainlit_client and res:
                # If cloud is enabled, store the response in the database/S3
                if spec.type == "text":
                    await self.process_user_message(res)
                elif spec.type == "file":
                    # TODO: upload file to S3
                    pass

            await self.clear_ask()
            return res
        except TimeoutError as e:
            await self.send_ask_timeout()

            if raise_on_timeout:
                raise e
        finally:
            await self.task_start()

    def update_token_count(self, count: int):
        """Update the token count for the UI."""

        return self.emit("token_usage", count)

    def task_start(self):
        """
        Send a task start signal to the UI.
        """
        return self.emit("task_start", {})

    def task_end(self):
        """Send a task end signal to the UI."""
        return self.emit("task_end", {})

    def stream_start(self, msg_dict: Dict):
        """Send a stream start signal to the UI."""
        return self.emit(
            "stream_start",
            msg_dict,
        )

    def send_token(self, id: str, token: str, is_sequence=False):
        """Send a message token to the UI."""
        return self.emit(
            "stream_token", {"id": id, "token": token, "isSequence": is_sequence}
        )

    def set_chat_settings(self, settings: Dict[str, Any]):
        self.session.chat_settings = settings
