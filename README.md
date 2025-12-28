
# 🔒 PortShieldGUI

**PortShieldGUI** is a powerful and user-friendly Python application built with **PyQt6**. It provides an intuitive graphical interface to manage Linux firewall rules (`iptables`), control system services (`systemctl`), and perform port scans using **nmap**.

---

## 📸 Interface Overview

---

## ✨ Features

### 🔥 Firewall Management
✅ Add rules with custom port, protocol, action, and optional IP filter  
✅ View and export active `iptables` INPUT rules  
✅ Flush rules with confirmation prompt  
✅ Block or unblock IP addresses  
✅ Perform quick `nmap` port scans  
✅ Auto-refresh rules every 10 seconds (optional)

### ⚙️ Service Manager
✅ Start/Stop services like SSH, Apache, FTP, and RDP  
✅ Scan ports to verify service availability  
✅ View real-time status updates

---

## 🖥️ User Interface

- **Dark Mode:** Sleek black theme (`#1e1e2f`) with white text
- **Custom Controls:** Green/Red buttons, input validation, and auto-refresh toggle
- **Tabbed Navigation:** Separate views for firewall and service control

---

## 📁 Project Structure

```
📦 PortShieldGUI
├── portshield_gui.py        # Main application file
├── requirements.txt         # Python dependencies
├── firewall_backup.rules    # Exported iptables rules
└── README.md                # Project documentation
```

---

## 📦 Requirements

| Dependency   | Description                       |
|--------------|------------------------------------|
| Python 3.8+  | Core language                     |
| PyQt6        | GUI framework                     |
| nmap         | Network scanning utility          |
| iptables     | Linux firewall utility            |
| systemctl    | Service management (systemd)      |
| sudo access  | Required for firewall/service control |

Install dependencies via:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

```bash
sudo python3 portshield.py
```

> ⚠️ Sudo/root access is required for firewall and service operations.

---

## ⚠️ Security Notice

- Incorrect iptables usage may lock you out of your own system
- Always test your firewall rules in a safe environment
- Configure `sudoers` for passwordless execution of specific commands if needed

---

## 📈 Future Improvements

- IPv6 (`ip6tables`) support
- Rule profile management (save/load sets)
- Real-time service monitoring & logs
- Custom user-defined rule builder

---

## 👨‍💻 Developed By

**JAS PREET**  
🔗 GitHub: [jaspreet-infosec](https://github.com/jaspreet-infosec)

