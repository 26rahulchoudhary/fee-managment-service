# Fee Management System

A cloud-native student fee management system built using Azure services. The system manages student fee records, calculates payment status, provides secure APIs, and automatically sends reminders for overdue fees.

## Overview

The Fee Management System provides:

* Student fee and payment tracking
* Automatic fee-status calculation
* Overdue fee detection
* Automated reminder emails
* Secure APIs through Azure API Management
* Microsoft Entra ID authentication and role-based access
* Admin operations for updating fee records
* SQL-based reporting and fee summaries

### Fee Status

The system calculates the payment status based on the total fee, paid amount, and due date.

* **Paid** — Full fee has been paid.
* **Partially Paid** — Payment is pending but the due date has not passed.
* **Overdue** — Payment is pending and the due date has passed.

---

## Azure Architecture

```text
                    Client / Postman
                           |
                           v
                Azure API Management
                 |                 |
                 |                 |
          Authentication       Rate Limiting
          Entra ID / JWT       Subscription Key
                 |
                 v
             API Backend
                 |
        +--------+--------+
        |                 |
        v                 v
 Azure Functions      Logic Apps
        |                 |
        |                 v
        |          Email Notifications
        |                 |
        +--------+--------+
                 |
                 v
          Azure SQL Database
                 |
        +--------+---------+
        |                  |
     Students         Administrators
```

---

# Azure Services

The project uses the following Azure services:

| Service              | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| Azure SQL Database   | Stores student and administrator fee records   |
| Azure Functions      | Provides API and fee-management business logic |
| Azure Logic Apps     | Automates overdue-fee notifications            |
| Azure API Management | Exposes and secures APIs                       |
| Microsoft Entra ID   | Authentication and role-based authorization    |
| Azure Storage        | Required by Azure Functions                    |
| Application Insights | Application monitoring and diagnostics         |

---

# Database

## Students Table

The `Students` table contains:

* `StudentID`
* `Name`
* `Course`
* `Email`
* `TotalFee`
* `PaidAmount`
* `DueDate`
* `CreatedAt`
* `UpdatedAt`

## Administrators Table

The `Administrators` table contains:

* `AdminID`
* `Name`
* `Email`
* `Role`
* `CreatedAt`

The database contains 20+ student records for testing and demonstration.

Database scripts are located in:

```text
sql/
├── schema.sql
└── seed.sql
```

---

# Azure Functions

Azure Functions provide the application's API and business logic.

## API Endpoints

### Get Student Fee

```http
GET /api/student/{student_id}/fee
```

Returns:

* Student details
* Total fee
* Paid amount
* Pending amount
* Due date
* Payment status

### Update Student Fee

```http
PUT /api/fee/admin/student/{student_id}
```

Allows authorized administrators to update the student's payment information.

### Get Students

```http
GET /api/students
```

Supports filtering by payment status and course.

### Fee Summary

```http
GET /api/summary
```

Returns overall fee collection and payment statistics.

### Health Check

```http
GET /api/health
```

Checks whether the application is running correctly.

---

# Automated Fee Notifications

Azure Logic Apps is used to automate overdue-fee reminders.

The workflow runs periodically and:

```text
Recurrence
    |
    v
Query Azure SQL
    |
    v
Find overdue students
    |
    v
For each student
    |
    v
Send reminder email
```

Students are selected when:

```text
DueDate < CurrentDate
AND
PaidAmount < TotalFee
```

The reminder contains the student's pending amount and original due date.

Email processing uses retry policies to improve reliability.

---

# API Management

Azure API Management provides the public API gateway.

Example endpoint:

```http
GET /fees/students/overdue
```

APIM provides:

* Subscription-key protection
* Rate limiting
* Authentication
* API routing
* Backend integration
* Request/response policies

Example public endpoint:

```text
https://fee-manage-api.azure-api.net/fees/students/overdue
```

---

# Authentication & RBAC

Microsoft Entra ID is used to secure protected APIs.

The application defines two main roles:

### Student

Allows students to access their fee information.

### Admin

Allows administrators to perform administrative fee operations.

APIM validates the Entra ID JWT before allowing requests to protected APIs.

The API also uses subscription keys and rate limiting as additional API-management controls.

---

# Project Structure

```text
fee-management-system/
│
├── api/
│   ├── admin_fee.py
│   ├── health.py
│   ├── student_fee.py
│   ├── students.py
│   └── summary.py
│
├── app/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── sql/
│   ├── schema.sql
│   └── seed.sql
│
├── function_app.py
├── host.json
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Local Setup

## 1. Create Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure Database

Create a `.env` file:

```env
DATABASE_SERVER=YOUR_SQL_SERVER.database.windows.net
DATABASE_NAME=YOUR_DATABASE_NAME
DATABASE_USERNAME=YOUR_SQL_ADMIN_USERNAME
DATABASE_PASSWORD=YOUR_SQL_ADMIN_PASSWORD
DATABASE_DRIVER=ODBC Driver 18 for SQL Server
```

Do not commit `.env` to Git.

## 4. Run Locally

```powershell
func start
```

The local Azure Functions host runs on:

```text
http://localhost:7071
```

---

# Deployment

The solution is deployed in phases.

## Phase 1 — Azure Infrastructure

Created:

* Resource Group
* Azure SQL Server
* Azure SQL Database
* Azure Storage Account

## Phase 2 — Database

Configured:

* SQL schema
* Student records
* Administrator records
* Constraints
* Indexes
* Seed data

## Phase 3 — Azure Functions

Implemented:

* Student fee API
* Admin fee update API
* Student listing API
* Fee summary API
* Health API

## Phase 4 — Business Logic

Implemented:

* Pending amount calculation
* Payment-status calculation
* Overdue detection
* Student/course filtering
* Fee summaries

## Phase 5 — Notifications

Configured Azure Logic Apps for:

* Daily overdue checks
* SQL query execution
* Student iteration
* Reminder emails
* Retry handling

## Phase 6 — API Management

Configured:

* APIM API
* Logic App backend
* Subscription-key protection
* Rate limiting
* Overdue-student API

## Phase 7 — Authentication & RBAC

Configured:

* Microsoft Entra ID application
* Student role
* Admin role
* API scope
* Test client application
* JWT validation through APIM

## Phase 8 — Monitoring & Final Deployment

Planned/configured as part of final deployment:

* Application Insights
* Error monitoring
* Retry policies
* Final security validation
* Deployment documentation
* Demo preparation

---

# Security

The project follows these security practices:

* Secrets are stored outside source control.
* `.env` and `local.settings.json` are excluded from Git.
* APIM subscription keys are required for protected API access.
* Entra ID JWT validation is used for authentication.
* Student and Admin roles provide role-based access.
* APIM rate limiting protects the API from excessive requests.
* Logic App callback URLs and SAS tokens must never be committed to Git.

---

# Documentation

Additional project documentation should contain:

```text
docs/
├── architecture.md
├── deployment.md
├── api.md
├── database.md
├── azure-services.md
└── demo.md
```

### Architecture Documentation

Explains:

* Overall solution architecture
* Azure services
* Data flow
* API flow
* Notification flow
* Authentication flow

### Deployment Documentation

Provides step-by-step instructions for:

1. Creating Azure resources
2. Configuring Azure SQL
3. Deploying Azure Functions
4. Configuring Logic Apps
5. Configuring API Management
6. Configuring Microsoft Entra ID
7. Assigning RBAC roles
8. Testing the complete system

---

# Development Phases

| Phase                         | Status      |
| ----------------------------- | ----------- |
| Azure Infrastructure          | Complete    |
| Azure SQL Database            | Complete    |
| Azure Functions APIs          | Complete    |
| Fee Business Logic            | Complete    |
| Automated Notifications       | Complete    |
| API Management                | Complete    |
| Entra ID & RBAC               | In Progress |
| Monitoring & Final Deployment | Pending     |

---

# Testing

The application can be tested using:

* Postman
* Azure Portal
* Azure SQL Query Editor
* Local Azure Functions runtime

Important scenarios include:

* Fully paid student
* Partially paid student
* Overdue student
* Admin fee update
* Unauthorized API request
* Missing subscription key
* Invalid JWT
* Rate-limit validation
* Automated overdue reminder

---

# Submission Deliverables

The final project will contain:

### Code

* Azure Functions source code
* Logic App configuration
* SQL schema and seed scripts
* API Management policies/configuration
* Authentication configuration

### Documentation

* Solution architecture
* Architecture diagram
* Database documentation
* API documentation
* Step-by-step Azure deployment guide
* Authentication and RBAC setup
* Testing instructions
* Demo instructions

---

# Important Notes

Never commit the following to the repository:

```text
.env
local.settings.json
API keys
subscription keys
client secrets
access tokens
Logic App SAS callback URLs
database passwords
```

The project is designed as a cloud-native Azure fee management system demonstrating **database management, serverless APIs, workflow automation, API security, authentication, RBAC, and monitoring**.
