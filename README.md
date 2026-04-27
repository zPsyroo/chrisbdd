# 🐾 Veterinary Clinic — CRUD Web Application

A full-stack CRUD web application for managing a veterinary clinic, built with Python Flask and MariaDB, deployed across two virtual machines.

## 🏗️ Architecture

| Machine | Role | IP |
|---------|------|----|
| VM1 | Flask Web Server | 192.168.1.152 |
| VM2 | MariaDB Database Server | 192.168.1.153 |

Public access is provided via **ngrok** instead of port forwarding, for security reasons.

## 🗄️ Database

5 tables with relationships:

- **duenos** — Pet owners
- **animales** — Animals (linked to owners)
- **veterinarios** — Vets
- **citas** — Appointments (linked to animals and vets)
- **tratamientos** — Treatments (linked to appointments)

### Database Users

| User | Permissions |
|------|------------|
| `flask_user` | SELECT, INSERT, UPDATE, DELETE |
| `admin_user` | ALL PRIVILEGES |

## ⚙️ Installation

### VM2 — Database Server
```bash
sudo apt install mariadb-server
sudo mysql -u root -p
# Paste the contents of veterinaria.sql
```

Allow external connections in `/etc/mysql/mariadb.conf.d/50-server.cnf`:
```
bind-address = 0.0.0.0
```

### VM1 — Web Server
```bash
sudo apt install python3 python3-pip
pip3 install flask mysql-connector-python --break-system-packages
```

Clone the repository and run:
```bash
python3 app.py
```

Expose with ngrok:
```bash
ngrok http 5000
```

## 🚀 Features

- ✅ Full CRUD on all 5 tables
- ✅ Relational data (foreign keys)
- ✅ Two database users with different permissions
- ✅ Distributed across two VMs
- ✅ Public access via ngrok

## 🛠️ Tech Stack

- Python 3 + Flask
- MariaDB
- HTML + CSS
- ngrok
- VirtualBox
