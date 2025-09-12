# 📖 Project Nexus - ProDev Backend Engineering

## 📌 Overview
Project Nexus is a **documentation hub** consolidating my major learnings from the **ProDev Backend Engineering program**.  
It highlights the backend technologies, concepts, challenges, and solutions I encountered, and serves as a **reference guide** for future learners.  

As a case study, I showcase my **Social Media Feed Backend** project — a scalable backend system that simulates real-world applications like Twitter or Instagram, with GraphQL APIs, CRUD operations, and user interactions.

---

## 🎯 Project Objective
- Consolidate **key learnings** from the ProDev Backend Engineering program.  
- Document **backend technologies, concepts, challenges, and solutions**.  
- Serve as a **knowledge hub** for backend learners.  
- Demonstrate collaboration between **frontend and backend developers**.  

---

## 🛠️ Key Technologies Covered
- **Python** (3.10+)  
- **Django** (backend framework)  
- **REST APIs** (Django REST Framework)  
- **GraphQL** (Graphene-Django)  
- **PostgreSQL** (relational database)  
- **Docker & docker-compose** (containerization)  
- **CI/CD Pipelines** (automation & deployment)  

---

## 📚 Important Backend Concepts
### 1. Database Design
- Normalization of data models.  
- Designing relationships for users, posts, comments, and likes.  
- Using indexes and constraints for performance.  

### 2. Asynchronous Programming
- Handling background tasks with **Celery + RabbitMQ**.  
- Examples: sending notifications, analytics jobs, scheduled tasks.  

### 3. Caching Strategies
- Using **Redis** for frequently accessed queries (e.g., feeds, trending posts).  
- Improving response times by avoiding repeated expensive queries.  

---

## ⚡ Case Study: Social Media Feed Backend
### Real-World Application
A backend system for managing posts, user interactions, and personalized feeds.  
Key learnings included:  
- Using **GraphQL** for flexible data fetching.  
- Designing schemas for **high-traffic user interactions**.  
- Optimizing queries and using **caching** for performance.  

### Goals
- **Post Management (CRUD):** Create, read, update, and delete posts.  
- **User Management (CRUD):** Manage profiles, authentication, and ownership of posts.  
- **Follow System:** Users can follow/unfollow others.  
- **Feed:** Personalized feed of posts from followed users, sorted by newest first.  
- **Interactions:** Users can like, comment, and share posts.  

---

## 📊 System Design

### Entity-Relationship Diagram (ERD)
```mermaid
erDiagram
    USER ||--o{ POST : "creates"
    USER ||--o{ FOLLOW : "follows"
    USER ||--o{ COMMENT : "writes"
    USER ||--o{ LIKE : "likes"

    POST ||--o{ COMMENT : "has"
    POST ||--o{ LIKE : "receives"

    USER {
        int id PK
        string username
        string email
        string password
        string bio
        string profile_picture
    }

    POST {
        int id PK
        string content
        string media_url
        datetime created_at
    }

    FOLLOW {
        int id PK
        int follower_id FK
        int following_id FK
    }

    COMMENT {
        int id PK
        string text
        datetime created_at
    }

    LIKE {
        int id PK
        datetime created_at
    }

### Workflow
```mermaid
flowchart TD
    A[User Registers/Login] --> B[Create Post]
    B --> C[Feed Updates]
    A --> D[Follow User]
    D --> C
    A --> E[Like/Comment Post]
    E --> C
    C --> F[GraphQL Feed Query]
    F --> G[Return Personalized Feed]

💻 Example GraphQL Queries
Create a User
mutation {
  createUser(username: "alice", email: "alice@mail.com", password: "12345") {
    user {
      id
      username
    }
  }
}
Fetch Personalized Feed
{
  feed(userId: 1) {
    id
    content
    author {
      username
    }
    createdAt
  }
}

🔑 Challenges & Solutions

Challenge: Optimizing feeds for large numbers of users.
Solution: Used query optimization + Redis caching.

Challenge: Handling background notifications.
Solution: Integrated Celery with RabbitMQ for async tasks.

Challenge: Ensuring authorization for mutations.
Solution: Implemented user ownership checks in GraphQL resolvers.

🏆 Best Practices & Takeaways

Write modular and clean code (apps, serializers, schema separation).

Always include unit tests to catch regressions early.

Use version control with clear commit messages (feat:, fix:, docs:).

Prioritize scalability: caching, async tasks, optimized queries.

Collaboration between frontend and backend learners ensures smooth integration.

🤝 Collaboration

Collaborated with ProDev Frontend learners who consumed the APIs.

Shared ideas and solutions in the #ProDevProjectNexus Discord channel and other relevant channels of communication.

Organized joint study sessions for debugging and API testing.

📅 Git Commit Workflow

feat: → new features (e.g., posts CRUD, follow system).

fix: → bug fixes.

perf: → performance improvements (query optimization).

docs: → README and documentation updates.

📊 Evaluation Criteria

Functionality – APIs for posts, users, and interactions.

Code Quality – clean, modular, well-structured code.

User Experience – intuitive GraphQL Playground.

Version Control – frequent commits with meaningful messages.


👩‍💻 Author

Ciiru Ngunjiri
ProDev Backend Engineer

GitHub: CiiruNgunjiri (https://github.com/CiiruNgunjiri)

Linkedin: Linda Ngunjiri (www.linkedin.com/in/linda-ngunjiri35)

Email: ciiru.ngunjiri@gmail.com
