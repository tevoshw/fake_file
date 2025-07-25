import subprocess
import time
import os
import pywifi
from pywifi import const
import winreg



def fake_file():

    
    ## 1.1 COMANDOs DE PROCURA DE APPS
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
    with open("apps_installed.txt", "a", encoding="utf-8") as f:
        for programa in programas:
            f.write(programa + "\n")
    

    
    ## 1.2 COMANDOS DE REDE INTERNET


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
    
    ### Checa se tem wifi ou ethernet
    wifi_info = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True).strip()
    if "SSID" in wifi_info:
        escanear_wifi()
        with open("wifi.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n\n {wifi_info}")
    else:
        wifi_info = subprocess.check_output("ipconfig /all", shell=True, text=True).strip()
        with open("wifi.txt", "a", encoding="utf-8") as f:
            f.write(wifi_info)
    

    ## 2 ATAQUES


    ### Criar e mostrar o 1 aviso de hacking (cmd)
    for x in range(5): # MUDAR PARA MAIS EM ATAQUES REAIS
        os.system(f'start cmd /k "echo OTARIO HACKED BY TEVO O SHOW https://x.com/estte7end https://x.com/estte7end https://x.com/estte7end"')
        time.sleep(1)
    #os.system("taskkill /f /im cmd.exe") # Deixar em comentário depois (usado apenas para testar e deixar mais facil)
    time.sleep(2)

    ### Criar e mostrar o 2 aviso de hacking (notas)
    with open("HACKEDBY.txt", "a", encoding="utf-8") as f:
        for x in range (10):
            f.write("OTARIO HACKED BY TEVO O SHOW\nhttps://x.com/estte7end\n")
    for x in range(5): #MUDAR PARA MAIS NÚMEROS EM ATAQUE REAL
        os.startfile("HACKEDBY.txt")
        time.sleep(1)
        os.system("taskkill /f /im notepad.exe")
    time.sleep(2)







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
    os.system("date /t & time /t")
    fake_file()
