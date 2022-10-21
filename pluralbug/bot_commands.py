from nio import AsyncClient, MatrixRoom, RoomMessageText

from pluralbug.chat_functions import react_to_event, send_text_to_room, set_displayname, delete_event, set_pfp
from pluralbug.config import Config
from pluralbug.storage import Storage


class Command:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        command: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """A command made by a user.

        Args:
            client: The client to communicate to matrix with.

            store: Bot storage.

            config: Bot configuration parameters.

            command: The command and arguments.

            room: The room the command was sent in.

            event: The event describing the command.
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        if self.command.startswith("echo"):
            await self._echo()
        elif self.command.startswith("sw"):
            await self._switch()
        elif self.command.startswith("re"):
            await self._react()
        elif self.command.startswith("del"):
            await self._delete()
        elif self.command.startswith("r"):
            await self._replace()
        elif self.command.startswith("help"):
            await self._show_help()
        elif self.command.startswith("pfp"):
            await self._set_pfp()
        else:
            await self._unknown_command()


    async def _set_pfp(self):
        if (len(self.args) < 2):
            await set_pfp(self.client, self.room.room_id, ''.join(self.args[0]))
        else:
            await set_pfp(self.client, self.room.room_id, ''.join(self.args[0]), ''.join(self.args[1:]))
        await delete_event(self.client, self.room.room_id, self.event.event_id)

    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _switch(self):
        """Set the display name"""
        name = " ".join(self.args)
        await set_displayname(self.client, name)
        await delete_event(
            self.client, self.room.room_id, self.event.event_id
        )
        await set_pfp(self.client, self.room.room_id, name)

    async def _react(self):
        """Make the bot react to the command message"""
        # React with a start emoji
        reaction = "⭐"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

    async def _delete(self):
        """Delete this message"""
        await delete_event(
            self.client, self.room.room_id, self.event.event_id
        )

    async def _replace(self):
        """Replace the command message as the bot"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)
        await delete_event(self.client, self.room.room_id, self.event.event_id)

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: "
            + "echo, switch (sw), react (re), delete (del), replace (r), help (h)"
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        return
        # await send_text_to_room(
        #     self.client,
        #     self.room.room_id,
        #     f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        # )
