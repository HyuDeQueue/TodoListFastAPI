# Todolist Project - FastAPI

## Overview
This project is a Todolist application built with FastAPI. It allows users to manage their daily tasks efficiently by providing functionalities like user authentication, task creation, task assignments, and group task management. The modular design ensures scalability and maintainability.

---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Documentation](#api-documentation)
4. [Environment Variables](#environment-variables)

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <project-directory>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the environment variables by creating a `.env` file based on the `.env.example` template.

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

---

## Usage
The application exposes RESTful endpoints for managing users, groups, tasks, and more. Use tools like Postman or cURL to test the endpoints.

Swagger UI is available at:
```
http://127.0.0.1:8000/docs
```

---

## API Documentation

### Authentication Router (`/api/auth`)
| **Endpoint**         | **Method** | **Description**  | **Status** |
|-----------------------|------------|------------------|------------|
| `/login`             | `POST`    | Login user       | ✅         |
| `/register`          | `POST`    | Register user    | ✅         |
|                       |            |                  |            |

---

### User Router (`/api/user`)
| **Endpoint**         | **Method** | **Description**      | **Status** |
|-----------------------|------------|----------------------|------------|
| `/`                 | `GET`     | Get all users        | ✅         |
| `/{user_id}`        | `GET`     | Get a specific user  | ✅         |
| `/{user_id}`        | `PUT`     | Update a specific user | ✅       |
| `/{user_id}`        | `DELETE`  | Ban a specific user  | ✅         |
|                       |            |                      |            |

---

### Group Router (`/api/group`)
| **Endpoint**         | **Method** | **Description**      | **Status** |
|-----------------------|------------|----------------------|------------|
| `/`                 | `POST`    | Create a group       | ✅         |
| `/`                 | `GET`     | Get all groups       | ✅         |
| `/{group_id}`       | `GET`     | Get a specific group | ✅         |
| `/{group_id}`       | `PUT`     | Update a group       | ✅         |
| `/{group_id}`       | `DELETE`  | Delete a group       | ✅         |
|                       |            |                      |            |

---

### Group Member Router (`/group-member`)
| **Endpoint**         | **Method** | **Description**     | **Status** |
|-----------------------|------------|---------------------|------------|
| `/add`              | `POST`    | Add a group member  | ✅         |
| `/delete`           | `DELETE`  | Delete a group member | ✅       |
| `/view`             | `GET`     | View group members  | ✅         |
|                       |            |                     |            |

---

### Task Router (`/api/router`)
| **Endpoint**         | **Method** | **Description**       | **Status** |
|-----------------------|------------|-----------------------|------------|
| `/user`             | `POST`    | Create a task for user | ✅         |
| `/group`            | `POST`    | Create a task for group| ✅         |
| `/task/{task_id}`   | `GET`     | Find a task by ID      | ✅         |
| `/user/{user_id}`   | `GET`     | Get tasks by user ID   | ✅         |
| `/group/{group_id}` | `GET`     | Get tasks by group ID  | ✅         |
| `/update/{task_id}` | `PUT`     | Update a task by ID    | ✅         |
| `/delete/{task_id}` | `DELETE`  | Delete a task by ID    | ✅         |
|                       |            |                       |            |

---

### Task Assignment Router (`/api/task_assign`)
| **Endpoint**         | **Method** | **Description**           | **Status** |
|-----------------------|------------|---------------------------|------------|
| `/assign/{task_id}/{user_id}` | `POST` | Assign a task to a user  | ✅         |
| `/update/{task_id}/{user_id}/to/{new_user_id}` | `PUT` | Reassign task to another user | ✅ |
| `/delete/{task_id}/{user_id}` | `DELETE` | Unassign a task from a user | ✅ |
|                       |            |                           |            |

---

## Environment Variables
| **Variable**     | **Description**                |
|-------------------|--------------------------------|
| `SECRET_KEY`      | Secret key for JWT encryption |
| `JWT_ALGORITHM`   | Algorithm for JWT             |
| `DATABASE_URL`    | Database connection string    |
| `JWT_EXPIRATION`  | JWT token expiration time     |

---


