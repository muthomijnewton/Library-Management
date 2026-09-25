# Library Management System

A Frappe-based Library Management System for managing library articles, members, memberships, and issue/return transactions.

## Overview

The Library Management System is a custom Frappe application designed to provide the core functionality required to manage a library.

The system allows library staff to:

* Manage library articles and their availability
* Register and manage library members
* Create and manage library memberships
* Configure loan periods and borrowing limits
* Issue and return articles
* Track article availability
* Validate active memberships before issuing articles
* Enforce the maximum number of articles a member can have issued
* Publish selected articles on the website

The application also includes a public-facing article catalogue where published articles can be viewed.

## Features

### Article Management

Articles contain information such as:

* Article name
* Author
* ISBN
* Publisher
* Description
* Image
* Publication status
* Availability status

Articles have two separate states:

* **Published** — controls whether the article is visible on the website
* **Available / Issued** — tracks whether the article is currently available for borrowing

### Library Members

The system maintains library member records containing:

* First name
* Last name
* Full name
* Email address
* Phone number
* Linked Frappe user account

Each library member can be associated with a Frappe user, allowing the system to connect website activity with a specific member.

### Library Memberships

Memberships define the period during which a member is allowed to borrow articles.

The system:

* Validates active memberships
* Prevents overlapping active memberships
* Automatically calculates the membership end date
* Uses the configured loan period from Library Settings

### Library Transactions

Library Transactions record article issue and return activities.

Supported transaction types:

* **Issue**
* **Return**

When an issue transaction is submitted:

```text
Article → Issued
```

When a return transaction is submitted:

```text
Article → Available
```

The system also handles transaction cancellation by reversing the corresponding article status.

### Borrowing Limits

The system supports a configurable maximum number of articles that a member can have issued at one time.

The limit is configured through **Library Settings**.

For example:

```text
Maximum Number of Issued Articles: 10
```

Before an article is issued, the system checks the member's current number of outstanding issues.

### Membership Validation

Before an article can be issued, the system verifies that the member has a valid submitted membership covering the transaction date.

If no valid membership exists, the transaction is rejected.

## Website

Published articles are available through the public website.

Example:

```text
/articles
```

Each published article can have its own detail page containing information about the article.

Website visibility is controlled independently from article availability.

For example:

| Published | Status    | Website                 |
| --------- | --------- | ----------------------- |
| Yes       | Available | Visible and available   |
| Yes       | Issued    | Visible but unavailable |
| No        | Available | Not publicly listed     |
| No        | Issued    | Not publicly listed     |

## Technology Stack

* **Frappe Framework**
* **Python**
* **MariaDB**
* **Redis**
* **JavaScript**
* **HTML/CSS**
* **Jinja Templates**

## Project Structure

```text
library_management/
├── library_management/
│   ├── library_management/
│   │   ├── doctype/
│   │   │   ├── article/
│   │   │   ├── library_member/
│   │   │   ├── library_membership/
│   │   │   ├── library_settings/
│   │   │   └── library_transaction/
│   │   └── ...
│   └── ...
├── hooks.py
├── modules.txt
├── patches.txt
└── pyproject.toml
```

## Core DocTypes

| DocType                 | Purpose                                             |
| ----------------------- | --------------------------------------------------- |
| **Article**             | Stores library article information and availability |
| **Library Member**      | Stores member information and linked user accounts  |
| **Library Membership**  | Manages member borrowing eligibility                |
| **Library Settings**    | Stores configurable library settings                |
| **Library Transaction** | Records article issue and return transactions       |

## Installation

This application is intended to run inside a Frappe Bench environment.

### 1. Get the application

From your Frappe Bench:

```bash
cd ~/frappe-bench/apps
git clone git@github.com:muthomijnewton/Library-Management.git library_management
```

### 2. Install the application

From the bench directory:

```bash
cd ~/frappe-bench
bench --site library.localhost install-app library_management
```

### 3. Migrate the site

```bash
bench --site library.localhost migrate
```

### 4. Start the development server

```bash
bench start
```

The application can then be accessed through the configured Frappe site.

For a local development setup using the Frappe development server:

```text
http://library.localhost:8000
```

## Configuration

Library-wide settings are managed through the **Library Settings** DocType.

Current configurable settings include:

### Loan Period

Defines the number of days for which a membership remains active.

### Maximum Number of Issued Articles

Defines the maximum number of articles a member can have issued simultaneously.

## Transaction Workflow

### Issue

```text
Member
   ↓
Valid Membership?
   ↓
Within Borrowing Limit?
   ↓
Article Available?
   ↓
Create Issue Transaction
   ↓
Submit Transaction
   ↓
Article → Issued
```

### Return

```text
Issued Article
   ↓
Create Return Transaction
   ↓
Submit Transaction
   ↓
Article → Available
```

### Cancellation

Cancelling an Issue transaction restores the article to:

```text
Available
```

Cancelling a Return transaction restores the article to:

```text
Issued
```

## Development

The application is developed using the Frappe Framework and follows the standard Frappe application structure.

Run migrations after DocType or schema changes:

```bash
bench --site library.localhost migrate
```

Start the development environment with:

```bash
bench start
```

## Testing

Frappe tests can be executed using:

```bash
bench --site library.localhost run-tests --app library_management
```

Specific DocType tests can also be run as needed during development.

## Future Improvements

Potential future improvements include:

* Website-based article issuing
* Member self-service pages
* Article search and filtering
* Borrowing history
* Due-date tracking
* Overdue notifications
* Email notifications
* Library reports and dashboards
* Improved website interface
* Role-based member portal
* Automated tests for additional business scenarios

## Project Status

The project currently includes the core library management functionality:

* Article management
* Library member management
* Membership management
* Library settings
* Issue and return transactions
* Transaction cancellation handling
* Membership validation
* Borrowing-limit validation
* Public article catalogue

Further development will extend the website functionality and member self-service capabilities.

## Author

**Newton Muthomi**

GitHub: [@muthomijnewton](https://github.com/muthomijnewton)

## License

This project is developed for educational and portfolio purposes.
