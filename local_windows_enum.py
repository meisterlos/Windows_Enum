import os
import subprocess
import datetime
import glob
import wmi

def get_hostname():
    return os.environ["COMPUTERNAME"]

def get_os_info():
    return subprocess.check_output(["systeminfo"], encoding="cp850").strip()

def get_users():
    return subprocess.check_output(["net", "user"], encoding="cp850").strip()

def get_installed_software():
    return subprocess.check_output(["wmic", "product", "get", "name,version"]).decode("utf-8").strip()

def get_proxy_settings():
    try:
        proxy = subprocess.check_output(["powershell", "(Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings').ProxyServer"], encoding="utf-8")
        return proxy.strip()
    except subprocess.CalledProcessError as e:
        return f"Error retrieving proxy settings: {e}"

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

def get_past_rdp_sessions():
    try:
        rdp_sessions = subprocess.check_output(
            [
                "powershell",
                "Get-WinEvent -LogName 'Microsoft-Windows-TerminalServices-LocalSessionManager/Operational' | Where-Object { $_.Id -eq 21 } | Select-Object -Property TimeCreated, Message | Format-List -Property *"
            ],
            encoding="utf-8"
        )
        return rdp_sessions.strip()
    except subprocess.CalledProcessError as e:
        return f"Error retrieving RDP session history: {e}"

def get_rdp_sessions():
    rdp_sessions = subprocess.check_output(["qwinsta"], encoding="cp850")
    return rdp_sessions.splitlines()



def get_previous_commands():
    c = wmi.WMI()  # WMI bağlantısı kur
    processes = c.Win32_Process()  # Tüm işlemleri sorgula
    commands = []
    for process in processes:
        command_line = process.CommandLine
        if command_line and command_line.strip():  # `None` değilse ve boş değilse ekle
            commands.append(command_line)
            if len(commands) >= 10:
                break
    return commands
    
def main():
    print("**Ana makine adı:**", get_hostname())
    print("**İşletim sistemi adı, mimarisi ve sürümü:**", get_os_info())
    print("**Makinedeki kullanıcıların listesi:**", get_users())
    print("**Kurulu yazılım envanteri:**", get_installed_software())
    print("**Proxy ayarlarının yapılandırılması:**", get_proxy_settings())
    print("**Kaydedilen PuTTY oturumları:**", get_putty_sessions())
    print("**PuTTY oturum içerikleri:**", get_putty_session_contents())
    print("**PuTTY SSH anahtarları:**", get_putty_ssh_keys())
    print("**PuTTY SSH anahtar içerikleri:**", get_putty_ssh_key_contents())
    print("**Geçmiş RDP oturumları:**", get_past_rdp_sessions())
    print("**Bağlı olduğu RDP oturumu:**", get_rdp_sessions())
    print("**Önceki çalıştırma komutlarının günlüğü:**", get_previous_commands())

if __name__ == "__main__":
    main()
