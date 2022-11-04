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
    - manage situation, when particular group admin attemting to pass validation
    ** functionalities has to return False (admin is not supposed to pass the validation)

    - manage situation, when in a particular group unvalidatied member is attempting to pass the validation
    ** if valdiation passed:
        - functionalities has disable restirctions for member for chat he came from
        - functionalities has update member validation status in according index in database (user)
        - functionalities has update group validated members list in according index in database (chat)

    ** if valdiation NOT passed:
        - functionalities has ban member for chat he came from
        - functionalities has update member validation status in according index in database (user)
        - functionalities has update group validated members list in according index in database (chat)

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

