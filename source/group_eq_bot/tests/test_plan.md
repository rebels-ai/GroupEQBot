
# Bot status updates

### Adding Bot into Supergroup 
 ⁃ Create | Update DB BotMetadata index entity
    - bot.status should be 'member'
 ⁃ Create | Update DB ChatNameIDMappings index entity

### Granting Bot in Supergroup admin rights
 ⁃ Update bot.status attribute in DB BotMetadata index entity
    - bot.status should be 'administrator'

### Demote/delete the bot from supergroup
 ⁃ Update bot.status attribute in DB BotMetadata index entity
    - bot.status should be 'left' | 'member' | 'restricted'


# Bot in supergroup behaviour

### Sending messages | adding members
 ⁃ Create | Update DB GroupEvents index
    - should be separate index dedicated to one chat

### Changing any member statuses 
 ⁃ Create | Update DB GroupEvents index
    - should be separate index dedicated to one chat
    - member previous status should be saved in db
        - change_historical_status: [{old_status: date}]
        - current_status: new_status


# New members in the supergroup

### New member joined
 ⁃ Create | Update GroupUsers index entity (create user in DB)
     - should be separate index dedicated to one chat
 ⁃ Create | Update DB GroupEvents index
 ⁃ Bot restricts user rights - changed to restrict all, bcse they dont need to pass validation in group chat anymore
 ⁃ Bot sends weclome message with link to private chat


# Private chat with bot

### Any user starts the bot in private chat
    - Bot send instruction for validation

### User clicks /start_validation
 ⁃ Read from ALL GroupUsers indeces whether new member ID is presented in index

#### User is not known by bot
    - Bot sends message 'i dont know you'

#### User is known by bot
 ⁃ Read chatNames from GroupChatIDMappings by chat_id
    - user already passed validation
        - bot sends messsage 'you already passed'
    - user did not pass the validation
        ⁃ bot sends generated buttons with chatNames
        ⁃ Create | Update BotEvents index

#### User starts validation with clicking the button
 - Update GroupUsers index (updated user.validation.start_time attribute)
 - Update BotEvents index with this event
 ⁃ Update BotEvents index with any user answers

#### User passed validation
 - Bot sends congrats to user
 - Bot disables restrictions in the group chat
 ⁃ Update GroupUsers index entity (update user status changed on member)
 ⁃ Update GroupUsers index entity (update user stop validation time)
 - Update GroupEvents index with change status event

#### User failed validation
 - Bot banns user in the group chat
 ⁃ Update GroupUsers index entity (update user status changed on banned)
 ⁃ Update GroupUsers index entity (update user stop validation time)
 - Update GroupEvents index with change status event
