# Validador de Dependências de Software

## 👥 Autores
- Paulo Vitor Fontes do Nascimento
- João Vitor Costa Leite Virginio da Silva

## 📋 Descrição
Projeto acadêmico para a disciplina de Teoria dos Grafos da UEMA. 
Sistema que detecta dependências circulares em módulos de software.

## 🚀 Como Usar
Para rodar o programa pelo código fonte .py voce deve ter instalado um compilador como o vs code com as bibliotecas python, abra o codigo nesse compilador e clique no botão run.
 - IMPORTANTE!!O programa vai pedir um arquivo de entrada .txt, que deve ser colocado na mesma pasta do código.
 - o arquivo .exe está dentro da pasta \dist\main.  
 - Se for rodar o código pelo arquivo .exe, os arquivos de entrada também deverão estar na mesma pasta, nesse caso, a pasta main.  
O arquivo de entrada deve estar no formato: 

D ou ND  
V1  V2 (com letras maiúsculas e separado por espaço)  
V3  V4  
...  

Exemplo:  
`D`   
`A  B`  
`B  D`  
`C  E`  
`E  F`  
`F  G`  

### Instalação
 - python v3.13.7 ou superior  
   https://www.python.org/downloads/  
 - biblioteca graphviz  
   (no cmd):  
   pip install graphviz   
