Here's the updated version with all the requested changes applied.

# Offline Point of Sale (POS) System for Small Businesses in Lesotho

## Overview

This project is a fully offline Point of Sale (POS) desktop application developed using **Python**, **Tkinter**, and **SQLite**. It was developed to put the knowledge and skills I acquired during my tertiary studies into practice by building a real-world software solution that addresses IT-related challenges faced by small businesses in Lesotho, while also creating an opportunity to generate income through locally developed software.

The system automates daily business operations including inventory management, sales processing, supplier management, user administration, receipt generation, reporting, and database backup while maintaining reliable transaction processing using ACID principles.

---

## Motivation

Many small businesses in Lesotho still rely on manual methods such as notebooks and calculators to record sales, manage inventory, and calculate profits. These approaches are time-consuming and prone to errors.

This project was developed to provide an affordable, practical, and fully offline solution that improves efficiency, reduces human error, supports informed business decision-making, and promotes locally developed software for Basotho businesses.

---

## Key Features

### User Management

* Secure user authentication
* Password hashing for secure credential storage
* Forced password change for first-time users
* Role-Based Access Control (RBAC)

  * Default Administrator
  * Administrator
  * Cashier
* Session management

---

### Product Management

* Add products
* Edit products
* Delete products
* Barcode support
* Product search
* Supplier assignment
* Stock quantity tracking
* Cost and selling price management

---

### Supplier Management

* Add suppliers
* Edit supplier information
* Delete suppliers
* View supplier records

---

### Sales Processing

* Barcode scanning
* Product search
* Shopping cart
* Quantity management
* Discount application
* Automatic stock deduction
* Cash payment processing
* Change calculation
* Receipt generation
* Automatic receipt numbering

---

### Inventory Management

* Automatic stock updates
* Low stock alerts
* Configurable low stock threshold
* Daily stock reports
* Monthly stock reports

---

### Reporting

* Daily sales reports
* Monthly sales reports
* Daily stock reports
* Monthly stock reports
* Profit and loss calculations
* Business insights

---

### Settings

* Business information management
* Receipt numbering configuration
* Inventory settings
* Backup settings

---

### Backup & Recovery

* Automatic database backups
* Manual backups
* Database restoration
* Backup history

---

## Software Engineering Concepts Demonstrated

This project demonstrates practical application of several software engineering principles including:

* Role-Based Access Control (RBAC)
* CRUD operations
* SQLite database design
* ACID transaction processing
* Exception handling
* Authentication and authorization
* Password hashing
* Data validation
* Backup and recovery
* Reporting and analytics
* Version control using Git and GitHub

---

## Technologies Used

| Technology         | Purpose                          |
| ------------------ | -------------------------------- |
| Python             | Application development          |
| Tkinter            | Desktop graphical user interface |
| SQLite             | Database management              |
| Git                | Version control                  |
| GitHub             | Source code hosting              |
| PyInstaller        | Application packaging            |
| Visual Studio Code | Development environment          |

---

## Project Structure

```text
POS_System/
│
├── assets/
├── auth/
├── database/
├── gui/
├── logs/
├── modules/
│   ├── inventory/
│   ├── products/
│   ├── reports/
│   ├── sales/
│   ├── settings/
│   ├── suppliers/
│   └── users/
├── receipts/
├── tests/
├── main.py
└── README.md
```

---

## Installation

1. Download the project as a ZIP file from GitHub.

2. Extract the ZIP file to your preferred location.

3. Open the project folder in Visual Studio Code or your preferred Python IDE.

4. Run the application:

```bash
python main.py
```

---

## Future Improvements

Planned enhancements include:

* Audit logging
* Customer management
* Credit sales
* Lay-buy functionality
* Mobile money integration
* Online payment integration
* Multi-branch support
* Cloud synchronization

---

## Current Status

Version 1 is substantially complete and includes the core functionality required for managing users, sales, inventory, suppliers, reporting, receipt generation, and database backup in a fully offline environment.

The audit logging module is the remaining planned feature for Version 1.

---

## Author

**Mpho George Makaliana**

Bachelor of Science in Computer Science

Email: [makalianamphogeorge@gmail.com](mailto:makalianamphogeorge@gmail.com)

---

## License

This project is shared for portfolio and educational purposes.

Copyright © 2026 Mpho George Makaliana. All rights reserved.