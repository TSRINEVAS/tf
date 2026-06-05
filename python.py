from datetime import date
import os
import platform
import shutil
import socket


def format_bytes(size):
    """Return a human-readable byte value."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def get_system_details():
    disk = shutil.disk_usage(os.getcwd())

    return {
        "date": str(date.today()),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "operating_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Unknown",
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd(),
        "disk_total": format_bytes(disk.total),
        "disk_used": format_bytes(disk.used),
        "disk_free": format_bytes(disk.free),
    }


def print_system_details():
    print("System Details")
    print("==============")
    for key, value in get_system_details().items():
        label = key.replace("_", " ").title()
        print(f"{label}: {value}")


if __name__ == "__main__":
    print_system_details()

