# Football LMS

**Football LMS** is a Django-based web application designed for managing football leagues and teams. It allows users to manage teams, matches, players, and more, providing a complete system for football league management.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

**Football LMS** is a Django web application for managing football leagues and teams. The application allows users to manage teams, create matches, track player statistics, and much more. It's built with Django and leverages the Django REST framework for APIs, making it a powerful and flexible system.

---

## Features

- User authentication via custom `CustomUser` model.
- Manage leagues and teams with CRUD operations.
- Match scheduling and management.
- Player statistics tracking.
- RESTful API for league and team management.
- JWT authentication for secure API access.
- Pagination for handling large data sets efficiently.

---

## Requirements

Before setting up the project, ensure you have the following dependencies installed:

- Python 3.8+
- Django 5.1.4
- djangorestframework 3.14.0
- djangorestframework-simplejwt 5.4.1

You can install these dependencies by running:

```bash
pip install -r requirements.txt

