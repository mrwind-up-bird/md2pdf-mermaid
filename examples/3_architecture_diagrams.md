# System Architecture

## Overview
This illustrates the microservices architecture for the payment processing system.

## Authentication Flow (Sequence Diagram)
```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database

    U->>F: Login Request
    F->>A: Validate Credentials
    A->>D: Query User
    D-->>A: User Data
    A-->>F: JWT Token
    F-->>U: Redirect to Dashboard
```

## Data Lifecycle (State Diagram)
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Developing
    Developing --> Testing
    Testing --> Staging
    Staging --> Production : Approve
    Staging --> Developing : Reject
    Production --> [*]
```

## Component Interaction (Class Diagram)
```mermaid
classDiagram
    class User {
        +String username
        +login()
        +logout()
    }
    class Session {
        +String tokenId
        +isValid()
    }
    User "1" *-- "many" Session : has
```
