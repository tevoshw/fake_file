# Projeto: Coleta de Informações e Avisos via Python

Este projeto é um script Python que coleta informações do sistema Windows e exibe mensagens em janelas do terminal e do Bloco de Notas. Também cria arquivos de texto com avisos personalizados. (MALWARE APENAS PARA ESTUDOS! SEM SEGUNDAS INTENÇÕES)

---

## O que o código faz

O script realiza as seguintes ações:

1. **Coleta informações do sistema** usando comandos do Windows (`netsh wlan show interfaces`, `ipconfig /all` entre outros) por meio de módulos como `subprocess, pywifi, winreg, os e time` e salva essas informações em uma variável.

2. **Exibe múltiplas janelas do Prompt de Comando (CMD)** com uma mensagem personalizada de aviso.

3. **Cria um arquivo de texto (`HACKEDBY.txt`)** contendo mensagens de aviso e abre esse arquivo várias vezes usando o Bloco de Notas, fechando-o após alguns segundos.

4. **Abre várias janelas do Bloco de Notas** em sequência e depois as fecha.

5. **Cria um arquivo de texto (`info.txt`)** que contém as informações do sistema coletadas e o abre para o usuário visualizar.

---

## Requisitos do sistema

- Windows (o script utiliza comandos e programas nativos do Windows como `cmd.exe` e `notepad.exe`).

---

## Como executar o script

- Execute o file.exe presente em /fake_file/dist/file.exe (ATENÇÃO AO EXECUTAR ESTARÁ SUJEITO AO CÓDIGO)
