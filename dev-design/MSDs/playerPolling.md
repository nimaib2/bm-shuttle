```mermaid
sequenceDiagram
    participant Admin Channel
    participant Player Channel 1
    participant Player Channel 2
    participant Twilio
    participant Scheduler
    participant Web Service
    participant Database
    
    Scheduler ->> Web Service: Trigger poll creation
    Web Service ->> Database: Create poll entity
    Web Service ->> Twilio: Send poll message to player
    Twilio ->> Player Channel 1: Send poll message to player
    Web Service ->> Scheduler: Schedule poll reminder task
    Web Service ->> Scheduler: Schedule poll lock task
    Player Channel 1 ->> Twilio: Player responds to poll message
    Twilio ->> Web Service: Player responds to poll message
    Web Service ->> Database: Create pollResponse entity
    Scheduler ->> Web Service: Trigger poll reminder
    Web Service ->> Twilio: Send reminder message to player
    Twilio->>Player Channel 2: Send reminder message to player
    Player Channel 1 ->> Twilio: Player responds to poll again 
    Twilio ->> Web Service: Player responds to poll again
    Web Service ->> Database: Update pollResponse entity
    Scheduler ->> Web Service: Trigger poll lock
    Web Service ->> Twilio: Send lock message to player
    Twilio->>Player Channel 2: Send lock message to player
    Web Service->> Twilio: Send lock message to admin
    Twilio->>Admin Channel: Send lock message to admin
    Player Channel 1 ->> Twilio: Player responds to poll again 
    Twilio ->> Web Service: Player responds to poll again
    Web Service ->> Twilio: Send 'poll locked' message to player
    Twilio->>Player Channel 1: Send 'poll locked' message to player

```