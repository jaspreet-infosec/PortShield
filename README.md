# <p align="center">🛡️ PortShieldGUI</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/Platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
</p>

---

## 📖 Introduction

**PortShieldGUI** is a robust, high-performance security dashboard designed for Linux administrators and security researchers. It provides a sleek, **Midnight-themed** graphical interface to orchestrate complex `iptables` rules, manage `systemd` services, and perform network reconnaissance via `nmap`—all without touching the terminal.

---

## ✨ Features

### 🔒 Firewall Orchestration

* **Dynamic Rule Creation:** Add rules by Port, Protocol (TCP/UDP), and Action (ACCEPT/DROP).
* **Precision Filtering:** Instantly block or allow specific Source IPs.
* **Live Monitoring:** Optional **10s Auto-Refresh** to watch rules update in real-time.
* **Persistence:** Export active rules to `.rules` files for backup and disaster recovery.

### ⚙️ Service Intelligence

* **One-Click Control:** Manage lifecycle (Start/Stop) for SSH (port 22), Apache2 (port 80), FTP/Vsftpd (port 21), and RDP/XRDP (port 3389).
* **Network Verification:** Integrated `nmap` engine to audit open ports and verify firewall efficacy.
* **System Integrity:** Real-time service status indicators.

---

## 🎨 Design & UX

* **Theme:** Carbon-Dark high-contrast interface (`#1e1e2f`).
* **Safety UX:** Color-coded destructive actions (Flush/Stop) with confirmation prompts.
* **Tabbed Architecture:** Seamless switching between Firewall and Service modules.

---

## 📂 Project Structure

```text
📦 PortShieldGUI
 ┣ 📜 portshield.py           # Core Application Logic
 ┣ 📜 requirements.txt        # Dependency Manifest
 ┣ 📜 firewall_backup.rules   # Auto-generated Rule Backups
 ┗ 📜 README.md               # Project Documentation
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites

Ensure you have the following system utilities installed:

* `iptables`
* `nmap`
* `systemd`

### 2. Python Environment Setup (Linux)

Create and activate a virtual environment to keep dependencies isolated:

```bash
# Install virtualenv if not installed
sudo apt install python3-venv -y

# Create a virtual environment named 'env'
python3 -m venv env

# Activate the virtual environment
source env/bin/activate
```

Install project dependencies inside the virtual environment:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To deactivate the environment when done:

```bash
deactivate
```

### 3. Execution

> [!IMPORTANT]
> Because `iptables` and `systemctl` modify system-level configurations, PortShieldGUI must be run with root privileges.

```bash
sudo python3 portshield.py
```

---

## ⚠️ Security Notice

* Incorrect firewall configuration can lead to system lockout.
* Always ensure you have an alternative access method before flushing rules.
* Use in a staging environment before deploying to production.

---

## 📌 Ports Used in PortShieldGUI

| Service      | Default Port |
| ------------ | ------------ |
| SSH          | 22           |
| Apache2      | 80           |
| FTP / Vsftpd | 21           |
| RDP / XRDP   | 3389         |

> These ports are used in the application for monitoring, firewall rules, and service management.

---

## 👨‍💻 Developed By

**JASPREET GREWAL**

<p align="left"> 
  <a href="https://github.com/jaspreet-infosec"> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Github"> </a>
  <a href="https://www.linkedin.com/in/jaspreet-infosec/"> <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"> </a>
</p>


<p align="center">Released under the MIT License. Contributions are welcome!</p>
