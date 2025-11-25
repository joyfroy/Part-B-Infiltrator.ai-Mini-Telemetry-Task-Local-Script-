# telemetry_gui.py
import tkinter as tk
from tkinter import ttk
import psutil
import subprocess

# --------------------------
# Telemetry Functions
# --------------------------
def get_open_port_count():
    result = subprocess.check_output("netstat -ano | findstr LISTENING", shell=True).decode()
    lines = result.strip().split("\n")
    return len(lines) if lines[0] else 0

def get_process_count():
    return len(psutil.pids())

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

def get_memory_usage():
    return psutil.virtual_memory().percent

def getSystemSnapshot():
    return {
        "memory": get_memory_usage(),
        "cpu": get_cpu_usage(),
        "processes": get_process_count(),
        "ports": get_open_port_count()
    }


# --------------------------
# GUI Dashboard
# --------------------------
class TelemetryDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Infiltrator.ai - System Telemetry Dashboard")
        self.geometry("480x400")
        self.configure(bg="#1b1b1b")

        title = tk.Label(
            self,
            text="Infiltrator.ai Telemetry Dashboard",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1b1b1b"
        )
        title.pack(pady=15)

        # Frame for metrics grid
        self.frame = tk.Frame(self, bg="#1b1b1b")
        self.frame.pack()

        # Metric cards
        self.cpu_card = self.create_card("CPU Usage (%)")
        self.memory_card = self.create_card("Memory Usage (%)")
        self.process_card = self.create_card("Running Processes")
        self.port_card = self.create_card("Open Ports")

        # Arrange cards in grid
        self.cpu_card.grid(row=0, column=0, padx=10, pady=10)
        self.memory_card.grid(row=0, column=1, padx=10, pady=10)
        self.process_card.grid(row=1, column=0, padx=10, pady=10)
        self.port_card.grid(row=1, column=1, padx=10, pady=10)

        # Start auto-refresh
        self.update_metrics()

    def create_card(self, title):
        """Creates a metric card widget."""
        card = tk.Frame(self.frame, bg="#2c2c2c", width=200, height=100)
        card.pack_propagate(False)

        label_title = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11, "bold"),
            fg="#cccccc",
            bg="#2c2c2c"
        )
        label_title.pack()

        label_value = tk.Label(
            card,
            text="--",
            font=("Segoe UI", 22, "bold"),
            fg="#4CC9F0",
            bg="#2c2c2c"
        )
        label_value.pack()

        card.value_label = label_value
        return card

    def update_metrics(self):
        """Refresh telemetry every second."""
        snap = getSystemSnapshot()

        self.cpu_card.value_label.config(text=f"{snap['cpu']}%")
        self.memory_card.value_label.config(text=f"{snap['memory']}%")
        self.process_card.value_label.config(text=snap["processes"])
        self.port_card.value_label.config(text=snap["ports"])

        self.after(1000, self.update_metrics)


# --------------------------
# Run Dashboard
# --------------------------
if __name__ == "__main__":
    app = TelemetryDashboard()
    app.mainloop()
