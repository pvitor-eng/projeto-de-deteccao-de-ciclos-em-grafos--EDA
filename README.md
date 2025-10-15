# Validador de Dependências de Software

## 👥 Autores
- Paulo Vitor Fontes do Nascimento
- João Vitor Costa Leite Virginio da Silva

## 📋 Descrição
Projeto acadêmico para a disciplina de Teoria dos Grafos da UEMA. 
Sistema que detecta dependências circulares em módulos de software.

## 🚀 Como Usar
O programa vai pedir um arquivo de entrada, que deve ser colocado na mesma pasta do código.
O arquivo de entrada deve estar no formato:

D ou ND  
V1  V2 (com letras maiúsculas e separado por espaço)  
V3  V4  
...  

Exemplo:  
D  
'A  B'  
"B  D"  
"C  E"  
"E  F"  
"F  G"  

### Instalação
pip install graphviz
