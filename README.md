# 🕷️ Malware Educacional - Coletor de Dados (Windows)

> ⚠️ **AVISO LEGAL:** Este projeto foi criado **exclusivamente para fins educacionais e de pesquisa em cibersegurança**. O autor **não se responsabiliza por qualquer uso indevido**. **Jamais utilize este programa em sistemas sem consentimento explícito.** Não possui fins políticos ou destrutivos.

---

## 📌 Descrição do Projeto

Este é um **malware educacional em formato `.exe`**, desenvolvido para **Windows 10**, que simula técnicas utilizadas por softwares maliciosos reais. O executável coleta diversos dados sensíveis de navegadores e do sistema operacional, com o objetivo de estudar vulnerabilidades locais e reforçar o entendimento sobre segurança digital.

---

## 🔧 Funcionalidades

- 💻 **Requisitos**: Windows 10 com **Chrome** ou **Opera GX/Stable** instalado.
- 🔑 Coleta de **senhas salvas** no navegador.
- 🍪 Extração de **cookies armazenados** no navegador.
- 🌐 Coleta de:
  - IP local e público
  - Nome da rede Wi-Fi conectada
  - Informações da conexão com a Internet
- 💽 Listagem de **aplicativos instalados no sistema**
- 📂 Armazenamento dos dados em arquivos separados (`.txt`, `.json`)
- ⚠️ Exibe **mensagens simulando um alerta de invasão**, via:
  - CMD (Prompt de Comando)
  - Notepad (Bloco de Notas)

---

## 📁 Saídas Geradas

O programa cria documentos com os seguintes dados:
- `senhas.txt` — senhas salvas descriptografadas
- `cookies.txt` — cookies extraídos dos navegadores
- `geral.txt` — IPs e conexão com a internet
- `wifi.txt` — dados sobre a rede sem fio conectada
- `apps.txt` — lista de programas instalados
- `hackedby.txt` — mensagem de aviso usada pelo malware

---

## 🐍 Bibliotecas Utilizadas

Projeto desenvolvido em **Python**, e convertido para `.exe` com ferramentas como **PyInstaller**.

Principais bibliotecas:
- `os`, `subprocess`, `shutil`, `json`, `base64`
- `sqlite3`, `win32crypt`, `socket`, `platform`
- `Crypto.Cipher` (PyCryptodome)

---

## ⚙️ Como Usar

> ⚠️ Execute **somente em ambiente controlado ou máquina virtual.**

1. Compile o script com `PyInstaller` (se quiser testar o `.py`):
   ```bash
   pyinstaller --noconsole --onefile malware_educacional.py
