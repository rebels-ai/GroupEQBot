# Use cases: Bot behaviour in group (supergroup)

## Bot Events

### Adding Bot into Supergroup
Description: Owner/admin of the group added the bot

System Action:

- Create | Update DB BotMetadata index entity

    Fields to be used:
    - bot_status: member
- Create | Update DB ChatNameIDMappings index entity

### Granting Bot in Supergroup admin rights
Description: Owner/admin of the group promoted the bot

System Action:
- Update DB BotMetadata index entity

    Fields to be used:
    - bot_status: administrator

### Demote/delete the bot from supergroup
Description:  Owner/admin of the group demoted/deleted the bot

System Action:
- Update DB BotMetadata index entity

    Fields to be used:
    - bot_status: 'left' | 'member' | 'restricted'

## Message Events

### User sent message
Description: User sent any type of messages (text, videop, audio, etc.).
             Bot should create separate index dedicated to one chat

System Action:
- Create | Update DB GroupEvents index

## Member Events

### User joined the group
Description: User joined the group either by himself or was added by member

System Action: 
- Create | Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{member: date}]
    - current_status: member
- Bot restricts user rights (see: use case - user was restricted)
- Bot sends weclome message with link to private chat

### User was restricted
Description: Bot restricts user right after he joined the group

System Action:
- Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{member: date}, {restricted: date}]
    - current_status: restricted

### User was unrestricted
Description: Bot unrestricts user right after he passed the validation

System Action:
- Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{member: date}, {restricted: date}, {member: date}]
    - current_status: member

### User was banned
Description: Bot bans user if validation was failed for corresponding group

System Action:
- Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{member: date}, {restricted: date}, {member: date}, {banned: date}]
    - current_status: banned

### User left the group after validation was passed
Description: User left the group after validation was passed

System Action:
- Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{left: date}]
    - current_status: left

### User left the group before validation was passed
Description: User left the group before validation was passed

System Action:
- Update DB GroupEvents index

    Fields to be used:
    - change_historical_status: [{restricted: date}]
    - current_status: restricted


# Use cases: Bot behaviour in private chat (1:1 with user)

### Any user starts the bot in private chat
Description: Any user starts the bot in private chat

System Action:
- Bot send instruction for validation

### User clicks /start_validation [1]
Description: User starts validation process with bot command

System Action:
```
Read from ALL GroupUsers indeces whether new member ID is presented in index

if user is not presented in bot's groups 
    Bot replies with message

elif user is presented
    Read chatNames from GroupChatIDMappings by chat_id

    if user already passed validation
        bot replies with messsage

    elif user did not pass the validation
        bot sends generated buttons with chatNames
        Create | Update DB BotEvents index
```

### User clicks /start_validation [2]
Description: Buttons from [1] appear if user hasn't passed the validation yet in chat where bot is present. User clicked one of the buttons.

System Action:
```
Update GroupUsers index
    Fields to be used:
    user.validation.start_time: date

Update BotEvents index with this event
Update BotEvents index with any user answers

if user passed validation:

    Bot replies with message
    Bot disables restrictions for corresponding group

    Update GroupUsers index entity
        Fields to be used:
        change_historical_status: [{member: date}, {restricted: date}, {member: date}]
        current_status: member

    Update GroupUsers index entity
        Fields to be used:
        user.validation.end_time: date

    Update GroupEvents index with change status event

elif user failed validation:

    Bot bans user in corresponding group

    Update GroupUsers index entity
        Fields to be used:
        change_historical_status: [{member: date}, {restricted: date}, {member: date}, {banned: date}]
        current_status: banned

    Update GroupUsers index entity
        Fields to be used:
        user.validation.end_time: date

    Update GroupEvents index with change status event
```