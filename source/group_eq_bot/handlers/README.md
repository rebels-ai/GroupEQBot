## Available handlers of telegram updates:

- `command handler`: responsible for handling command messages like `/command`

- `text message handler`: responsible for handling text messages, excluding commands

- `audio message handler`: handles updates with audio and voice messages

- `video message handler`: handles messages, containing videos, video notes, stickers, animations and photos

- `document message handler`: handles messages with any types of files attached to them

- `chat member handler`: responsible for handling updates with any status changes of chat members, where bot is present

- `conversation validation handler`: responsible for the validation procedure. Once member sent `/start` command, all following messages will be processed by this handler until validation ended or stopped manually.