# PKI descentralizada

O projeto consiste em um sistema distribuído, descentralizado, como alternativa à Infraestrutura de Chaves Públicas (PKI, ou Public Key Infrastructure) tradicional, baseada em Autoridades Certificadoras (AC) hierárquicas.
Foi utilizado a implementação de sistemas Web3, mais especificamente a tecnologia Cartesi e blockchain baseada na Ethereum Virtual Machine (EVM).

## Índice

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configuração do ambiente](#configuracao-ambiente)
- [Instalação](#instalação)
- [Uso](#uso)

## Tecnologias Utilizadas

- Python
- Cartesi
- Ethereum Virtual Machine (EVM)
- Docker

## Configuração do ambiente

# Instalar o Docker
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
docker --version

# Instalar o Cartesi
npm install -g @cartesi/cli

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nome-do-repositorio.git

# Navegue até o diretório do projeto
cd nome-do-repositorio

# Instale as dependências
npm install # ou o comando correspondente para sua tecnologia

# Com o Docker em execução, faça o build do Cartesi:
cartesi build

## Uso

# Para iniciar o Cartesi:
cartesi run

# Para enviar entradas genéricas para a aplicação (Em um novo terminal e mantendo o anterior aberto):
cartesi send generic
### Teclar Enter até o momento de Input String

# A entrada deverá ser no seguinte formato:
