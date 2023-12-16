# Vendor System API

A Vendor Management System(VMS) apis  for efficient vendor profile management, purchase order tracking, and vendor performance metrics calculation.

![Python version](https://img.shields.io/badge/Python-3.9-4c566a?logo=python&&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django version](https://img.shields.io/badge/Django-4.2.7-4c566a?logo=django&&longCache=truelogoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django-RestFramework version](https://img.shields.io/badge/Django_Rest_Framework-3.14.0-red.svg?longCache=true&style=flat-square&logo=django&logoColor=white&colorA=4c566a&colorB=pink)  ![Last Commit](https://img.shields.io/github/last-commit/bhaveshdev09/vendor-hub-api/master?&&longCache=true&logoColor=white&colorB=green&style=flat-square&colorA=4c566a)

## Table of Contents

- [Core Features](#features)
- [Project Plan](#planning)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)



## Core Features

1. **Vendor Profile Management:**

   - Create, retrieve, update, and delete vendor profiles.
   - Track vendor information including name, contact details, address, and a unique vendor code.
2. **Purchase Order Tracking:**

   - Create, retrieve, update, and delete purchase orders.
   - Track purchase order details such as PO number, vendor reference, order date, items, quantity, and status.
3. **Vendor Performance Evaluation:**

   - Calculate vendor performance metrics, including on-time delivery rate, quality rating average, average response time, and fulfillment rate.
   - Retrieve performance metrics for a specific vendor.

## Project Plan 

To access the project plan, please visit the following URL: [Vendor System API](https://github.com/NirenPatel738/vendorsystem)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nirenpatel738/vendorsystem.git
   cd backend
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv virtualenv
   source virtualenv/bin/activate  # On Windows, use `virtualenv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```
4. Run the development server:

   ```bash
   python manage.py runserver
   ```
5. Set the environment variables
   
   > Please refer **.env.example** for must have variables

6. Access the application at http://localhost:8000.

## API Endpoints

Below is a summary of the available API endpoints:

**Vendor Profile Management**

| Endpoint               | Method      | Description                           |
| ---------------------- | ----------- | ------------------------------------- |
| `/api/vendors/register/`      | POST        | Create a new vendor.                  |
| `/api/vendors/login/`      | POST        | Login vendor.                  |
| `/api/vendors/vendors_list/`      | GET         | List all vendors.                     |
| `/api/vendors/vendor_profile/{id}/` | GET         | Retrieve a specific vendor's details. |
| `/api/vendors/update_profile/{id}/` | PUT / PATCH | Update a vendor's details.            |
| `/api/vendors/logout/` | DELETE      | Logout a vendor.                      |
| `/api/vendors/vendor_delete/{id}/` | DELETE      | Delete a vendor.                      |

**Purchase Order Tracking**

| Endpoint                                  | Method       | Description                                    |
| ----------------------------------------- | ------------ | ---------------------------------------------- |
| `/api/order/purchase_orders/`                 | POST         | Create a purchase order.                       |
| `/api/order/purchase_orders_list/`                 | GET          | List all purchase orders.                      |
| `/api/order/purchase_orders_retrive/{id}/`            | GET          | Retrieve details of a specific purchase order. |
| `/api/order/purchase_orders_update/{id}/`            | PUT / PATCH  | Update a purchase order.                       |
| `/api/order/purchase_orders_delete/{id}/`            | DELETE       | Delete a purchase order.                       |
| `/api/order/purchase_orders/{id}/acknowledge` | POST | Acknowledge a purchase order.                  |

**Vendor Performance Evaluation**

| Endpoint                                  | Method | Description                              |
| ----------------------------------------- | ------ | ---------------------------------------- |
| `/api/order/vendors/{id}/performance`         | GET    | Retrieve a vendor's performance history. |


