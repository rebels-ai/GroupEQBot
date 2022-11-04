Situation:
    2 types of output: 
        - events (manageable by interface) comes from group chats
        - validation events comes from ConversationHandler (private user:bot chats)
    We need interface for storing those events and reading them

    group chats
        users --> events
              --> validation events * adjust interface to skip them

    bot chats
        users --> validation events
              --> events * adjust interface to skip them

Tasks:

    * get one user's event from one group chat
    * get many user's event from one group chat

    * get one user's event from many group chats
    * get many user's event from many group chats

    * get one user's event from bot chat
    * get many user's event from bot chats



Description:
    Multiple Indeces containing list of users for according group and their metadata including validation info
GroupUsers
    user1
        userName
            []
        userID
        validation passed True/False
        status updates
            timestamp
                new_status
                old_status
            timestamp
                new_status
                old_status
        userMetrics
            ...

Users
    user1
        userName
        userID
        chats
            chat
                validation passed
                userMetrics
                status updates
                    timestamp
                        new_status
                        old_status
            chat
                validation passed
                userMetrics


Description:
    Multiple Indeces for storing events for particular group chat
GroupChat
    event
        eventID
        eventTime
        eventType
        userMetadata
        content
        contentMetadata
 …

Description:
    Single Index for storing validation events for every user in any chat
    Multiple Indeces for storing validation events for every user in particular chat
BotChat
    chat
        user
            event
                eventID
                eventType
                userMetadata
                content
                contentMetadata

        user
            event
                eventID
                eventType
                userMetadata
                content
                contentMetadata
                 ….

    chat
        ….


Description:
    Single Index for keeping bot information:
        - Where bot was added
        - If bot is an Admin
BotMetaData


* find get_chat_member
* does get_chat_members works for bots?


Functionality to glue indeces 
User can start validation if following are True:

    - Bot and user are in the same group chat (Implement BotMetaData Index)
        Questions:
            How to check in which groups bot is added and is admin?
            How to get list of all group members?
                We plan to use UserIndex
                Or bot methods if allowed
        Potential use cases:
        - User joined after bot was added to the group
        - User joined before the bot was added to the group

    - User hadn't started the validation
        Questions:
            How to check that user did not start the validation?
                We plan to use UserIndex