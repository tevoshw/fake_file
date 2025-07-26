# 🛑 Python Malware Educacional — Coletor de Dados do Windows (Opera GX)

> ⚠️ Este projeto tem **fins estritamente educacionais** para quem estuda cibersegurança, análise forense e engenharia reversa. Não me responsabilizo por qualquer uso indevido.

---

## 📌 Descrição

Este script em Python simula o comportamento de um malware de coleta de dados em sistemas Windows. Ele é capaz de extrair e armazenar informações sensíveis locais, como:

- Cookies e senhas salvas no navegador **Opera GX**
- Informações avançadas sobre a rede Wifi/Ethernet (no futuro, possibilidade de desconectar e mudanças)
- Aplicativos instalados
- Dados do sistema operacional
- Mensagens de alerta do sistema hackeado juntamente com meu X

---

## 🔧 Tecnologias e Bibliotecas Utilizadas

- `os` – manipulação de sistema de arquivos
- `subprocess` – execução de comandos do sistema
- `sqlite3` – leitura de bancos de dados locais dos navegadores
- `base64` e `json` – decodificação de chaves e dados do navegador
- `Cryptodome` – descriptografia AES de dados
- `shutil` – cópia de arquivos temporários
- `win32crypt` (fallback para versões antigas)
- Entre outras...

---

## ⚙️ Funcionalidades

| Módulo               | Descrição                                                                 |
|----------------------|--------------------------------------------------------------------------|
| Coleta de Cookies    | Acessa o banco SQLite do Opera GX e descriptografa cookies salvos        |
| Coleta de Senhas     | Extração de senhas salvas via descriptografia da chave local             |
| Coleta de IP         | Captura o IP público e local da máquina                                  |
| Nome da Rede Wi-Fi   | Mostra qual rede Wi-Fi está conectada no momento                         |
| Aplicativos Instalados | Lista todos os apps instalados com nome e caminho                      |

---

## 🖥️ Requisitos

- Sistema operacional: **Windows 10 ou 11**
- Navegador: **Opera GX instalado e ativo** (em breve terá a opção do chrome e outros navegadores)

```bash
pip install pycryptodome pypiwin32
