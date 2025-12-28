import sys
import subprocess
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox, QTabWidget, QGridLayout,
    QGroupBox, QCheckBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer


def validate_ip(ip):
    return re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip)


def validate_port(port):
    return port.isdigit() and 0 < int(port) <= 65535


class PortShieldGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PortShield - Enhanced Firewall & Service Manager")
        self.setGeometry(100, 100, 950, 800)
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2f; color: #ffffff; font-size: 14px; }
            QPushButton { padding: 6px 12px; border-radius: 5px; background-color: #2e2e3f; color: #ffffff; }
            QPushButton:hover { background-color: #3e3e5f; }
            QLineEdit, QTextEdit, QComboBox { background-color: #2b2b3d; color: #ffffff; border: 1px solid #444; padding: 4px; border-radius: 4px; }
            QGroupBox { border: 1px solid #555; border-radius: 6px; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0px 5px 0px 5px; }
        """)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_firewall_tab(), "🔒 Firewall")
        self.tabs.addTab(self.create_services_tab(), "🛠️ Services")
        layout.addWidget(self.tabs)

        # Auto-refresh toggle
        self.auto_refresh = QCheckBox("Auto Refresh Rules (every 10s)")
        self.auto_refresh.setStyleSheet("margin-left: 10px;")
        self.auto_refresh.stateChanged.connect(self.toggle_auto_refresh)
        layout.addWidget(self.auto_refresh)

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_rules)

        self.setLayout(layout)

    def toggle_auto_refresh(self, state):
        if state == Qt.CheckState.Checked.value:
            self.timer.start(10000)
        else:
            self.timer.stop()

    def create_firewall_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        rule_box = QGroupBox("Create Firewall Rule")
        rule_layout = QGridLayout()

        rule_layout.addWidget(QLabel("Protocol:"), 0, 0)
        self.proto_box = QComboBox()
        self.proto_box.addItems(["tcp", "udp"])
        rule_layout.addWidget(self.proto_box, 0, 1)

        rule_layout.addWidget(QLabel("Port:"), 1, 0)
        self.port_input = QLineEdit()
        rule_layout.addWidget(self.port_input, 1, 1)

        rule_layout.addWidget(QLabel("Action:"), 2, 0)
        self.action_box = QComboBox()
        self.action_box.addItems(["ACCEPT", "DROP", "REJECT"])
        rule_layout.addWidget(self.action_box, 2, 1)

        rule_layout.addWidget(QLabel("Source IP (optional):"), 3, 0)
        self.ip_filter_input = QLineEdit()
        rule_layout.addWidget(self.ip_filter_input, 3, 1)

        self.add_btn = QPushButton("Add Rule")
        self.add_btn.clicked.connect(self.add_rule)
        rule_layout.addWidget(self.add_btn, 4, 0, 1, 2)

        rule_box.setLayout(rule_layout)
        layout.addWidget(rule_box)

        # Firewall controls
        ctrl_box = QGroupBox("Firewall Controls")
        ctrl_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Rules")
        self.refresh_btn.clicked.connect(self.load_rules)
        self.flush_btn = QPushButton("Flush All Rules")
        self.flush_btn.setStyleSheet("background-color: #aa3333;")
        self.flush_btn.clicked.connect(self.flush_rules)
        self.save_btn = QPushButton("Export Rules")
        self.save_btn.clicked.connect(self.export_rules)
        ctrl_layout.addWidget(self.refresh_btn)
        ctrl_layout.addWidget(self.flush_btn)
        ctrl_layout.addWidget(self.save_btn)
        ctrl_box.setLayout(ctrl_layout)
        layout.addWidget(ctrl_box)

        # Rules display
        self.rules_display = QTextEdit()
        self.rules_display.setReadOnly(True)
        layout.addWidget(QLabel("Current iptables Rules:"))
        layout.addWidget(self.rules_display)

        # IP blocker
        block_box = QGroupBox("Block / Unblock IP")
        block_layout = QHBoxLayout()
        self.block_ip_input = QLineEdit()
        self.block_ip_input.setPlaceholderText("Enter IP to block/unblock")
        block_btn = QPushButton("Block")
        unblock_btn = QPushButton("Unblock")
        block_btn.clicked.connect(self.block_ip)
        unblock_btn.clicked.connect(self.unblock_ip)
        block_layout.addWidget(self.block_ip_input)
        block_layout.addWidget(block_btn)
        block_layout.addWidget(unblock_btn)
        block_box.setLayout(block_layout)
        layout.addWidget(block_box)

        # Nmap scan
        scan_box = QGroupBox("Port Scan")
        scan_layout = QHBoxLayout()
        self.nmap_ip_input = QLineEdit()
        self.nmap_ip_input.setPlaceholderText("Target IP")
        self.nmap_btn = QPushButton("Scan")
        self.nmap_btn.clicked.connect(self.run_nmap)
        scan_layout.addWidget(self.nmap_ip_input)
        scan_layout.addWidget(self.nmap_btn)
        scan_box.setLayout(scan_layout)
        layout.addWidget(scan_box)

        self.nmap_result = QTextEdit()
        self.nmap_result.setReadOnly(True)
        layout.addWidget(QLabel("Scan Result:"))
        layout.addWidget(self.nmap_result)

        tab.setLayout(layout)
        self.load_rules()
        return tab

    def create_services_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Manage System Services")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(10)
        headers = ["Service", "Enable", "Disable", "Status"]
        for i, text in enumerate(headers):
            grid.addWidget(QLabel(f"<b>{text}</b>"), 0, i)

        self.services = {
            "ssh": "22",
            "apache2": "80",
            "vsftpd": "21",
            "xrdp": "3389"
        }
        self.status_labels = {}

        for row, (svc, port) in enumerate(self.services.items(), start=1):
            grid.addWidget(QLabel(svc), row, 0)
            enable_btn = QPushButton("Enable")
            disable_btn = QPushButton("Disable")
            status_lbl = QLabel("unknown")
            enable_btn.clicked.connect(lambda _, s=svc: self.toggle_service(s, "start"))
            disable_btn.clicked.connect(lambda _, s=svc: self.toggle_service(s, "stop"))
            grid.addWidget(enable_btn, row, 1)
            grid.addWidget(disable_btn, row, 2)
            grid.addWidget(status_lbl, row, 3)
            self.status_labels[svc] = status_lbl
            self.update_service_status(svc)

        layout.addLayout(grid)
        tab.setLayout(layout)
        return tab

    def toggle_service(self, service, action):
        subprocess.run(["sudo", "systemctl", action, service], capture_output=True)
        self.update_service_status(service)

    def update_service_status(self, service):
        result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True)
        status = result.stdout.strip()
        self.status_labels[service].setText(status)

    def add_rule(self):
        proto = self.proto_box.currentText()
        port = self.port_input.text().strip()
        action = self.action_box.currentText()
        src_ip = self.ip_filter_input.text().strip()
        if not validate_port(port):
            QMessageBox.warning(self, "Input Error", "Invalid port.")
            return
        if src_ip and not validate_ip(src_ip):
            QMessageBox.warning(self, "Input Error", "Invalid IP address.")
            return

        cmd = ["sudo", "iptables", "-A", "INPUT"]
        if src_ip:
            cmd += ["-s", src_ip]
        cmd += ["-p", proto, "--dport", port]
        if action == "REJECT":
            cmd += ["-j", "REJECT", "--reject-with", "icmp-port-unreachable"]
        else:
            cmd += ["-j", action]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", f"Rule added for port {port}.")
            self.load_rules()
        else:
            QMessageBox.critical(self, "Command Failed", result.stderr)

    def load_rules(self):
        result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-n", "--line-numbers"], capture_output=True, text=True)
        self.rules_display.setText(result.stdout if result.returncode == 0 else result.stderr)

    def flush_rules(self):
        if QMessageBox.question(self, "Confirm", "Flush all INPUT rules?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            subprocess.run(["sudo", "iptables", "-F", "INPUT"], capture_output=True)
            self.load_rules()

    def export_rules(self):
        result = subprocess.run(["sudo", "iptables-save"], capture_output=True, text=True)
        if result.returncode == 0:
            with open("firewall_backup.rules", "w") as f:
                f.write(result.stdout)
            QMessageBox.information(self, "Saved", "Rules exported to firewall_backup.rules")
        else:
            QMessageBox.critical(self, "Error", result.stderr)

    def run_nmap(self):
        ip = self.nmap_ip_input.text().strip()
        if not validate_ip(ip):
            QMessageBox.warning(self, "Error", "Invalid IP.")
            return
        result = subprocess.run(["nmap", "-Pn", ip], capture_output=True, text=True)
        self.nmap_result.setText(result.stdout if result.returncode == 0 else result.stderr)

    def block_ip(self):
        ip = self.block_ip_input.text().strip()
        if not validate_ip(ip):
            QMessageBox.warning(self, "Input Error", "Enter a valid IP.")
            return
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], capture_output=True)
        self.load_rules()

    def unblock_ip(self):
        ip = self.block_ip_input.text().strip()
        if not validate_ip(ip):
            QMessageBox.warning(self, "Input Error", "Enter a valid IP.")
            return
        subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], capture_output=True)
        self.load_rules()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = PortShieldGUI()
    gui.show()
    sys.exit(app.exec())
