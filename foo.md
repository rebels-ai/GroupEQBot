What we need to save:
    - all incoming events
        - public chat
        - private bot:user chats (validation)
    - user info
        - chat ids
        - user metrics
        - validation passed
        - validation answers
    - chat info
        - members list
        - members who passed validation

Indeces:
    - Validation index (bot:user private chat)


1. Carry over button logic to it's dedicated place (check components folder)
2. Re-iterate member statuses logic
3. Add logic for /start button
4. Update storage.interface docstrings



ConversationHandler
    - manage situation, when in a particular group VALIDATED member is attempting to pass the validation
    ** check new index for bot (validating process)

    ** if member passed

    - manage situation when user blocked --> going to priv chat with bot and passes the validation

    - manage creating new index for bot (validating process)
        ** add conversation (validation) history
        ** should be single (static) index
            - user id
            - chat id (where user is trying to pass validation)
            - user + user start validation time + user end validation time + user cancel validation time
            ...

    - manage situation, when in a particular group VALIDATED member is attempting to pass the validation
    ** check new index for bot (validating process)

    ** if member passed

    - manage situation when user blocked --> going to priv chat with bot and passes the validation

    - manage creating new index for bot (validating process)
        ** add conversation (validation) history
        ** should be single (static) index
            - user id
            - chat id (where user is trying to pass validation)
            - user + user start validation time + user end validation time + user cancel validation time
            ...
