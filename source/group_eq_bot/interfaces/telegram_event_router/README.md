# Router

Router receives incoming Telegram events from registered handlers:

    - Bot Handler
    - Member Handler
    - Message Handlers 
        - Audio
        - Document
        - Text
        - Video

Note: *Conversation Handler bypasses router, because it needs it's own handlers as entrypoints or states*

Then events is routed to Public | Private EventProcessors, depending on ChatType of the received event.
