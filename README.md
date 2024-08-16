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

### Instalar o Docker
Atualize os pacotes
```bash
sudo apt-get update
```
Instale pacotes necessários
```bash
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```
Adicione a chave GPG do Docker
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
Adicione o repositório do Docker
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
Atualize novamente os pacotes
```bash
sudo apt-get update
```
Instale o Docker
```bash
sudo apt-get install docker-ce
```
Verifique a instalação
```bash
docker --version
```
### Para o funcionamento do Cartesi, é necessário instalar o suporte para Docker RISC-V
```bash
sudo chmod 666 /var/run/docker.sock
```
```bash
docker run --privileged --rm tonistiigi/binfmt:riscv
```
### Instalar o Cartesi
```bash
sudo npm install -g @cartesi/cli
```

### Caso precise atualizar o node para uma versão mais recente (22 neste caso)
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc  # or source ~/.zshrc
nvm install 22
```


## Instalação

### Clone o repositório
```bash
git clone https://github.com/gustavo-b-nahuz/Cartesi-PKI.git
```

### Navegue até o diretório do projeto
```bash
cd Cartesi-PKI
```

### Instale as dependências
```bash
npm install # ou o comando correspondente para sua tecnologia
```

### Com o Docker em execução, faça o build do Cartesi:
```bash
cartesi build
```

## Uso

### Para iniciar o Cartesi:
```bash
cartesi run
```

### Para enviar entradas genéricas para a aplicação (Em um novo terminal e mantendo o anterior aberto):
```bash
cartesi send generic
```

### Teclar Enter até o momento de Input String

### A entrada deverá ser no seguinte formato:

