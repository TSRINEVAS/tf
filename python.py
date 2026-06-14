from datetime import date
import argparse
import ctypes
import os
import platform
import shutil
import socket
import sys
import time


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


def turn_off_screen():
    if platform.system() != "Windows":
        raise RuntimeError("Turning off the screen is currently supported on Windows only.")

    hwnd_broadcast = 0xFFFF
    wm_syscommand = 0x0112
    sc_monitorpower = 0xF170
    monitor_off = 2

    ctypes.windll.user32.PostMessageW(
        hwnd_broadcast,
        wm_syscommand,
        sc_monitorpower,
        monitor_off,
    )


def schedule_screen_off(minutes):
    seconds = minutes * 60
    print(f"Screen will turn off in {minutes} minute(s).")
    print("Keep this script running. Press Ctrl+C to cancel.")
    time.sleep(seconds)
    turn_off_screen()
    print("Screen off command sent.")


def parse_args():
    parser = argparse.ArgumentParser(description="Show system details or turn off the screen after a delay.")
    parser.add_argument(
        "--screen-off",
        type=float,
        metavar="MINUTES",
        help="turn off the screen after the given number of minutes",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    try:
        if args.screen_off is None:
            print_system_details()
        elif args.screen_off <= 0:
            print("Minutes must be greater than 0.", file=sys.stderr)
            sys.exit(1)
        else:
            schedule_screen_off(args.screen_off)
    except KeyboardInterrupt:
        print("\nScreen off timer canceled.")

