![image](https://github.com/user-attachments/assets/dee6c3c8-01d2-4dc6-923a-9f7d0a156c5b)# PKI descentralizada

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
```bash
> cartesi send generic
? Chain Foundry
? RPC URL http://127.0.0.1:8545
? Wallet Mnemonic
? Mnemonic test test test test test test test test test test test junk
? Account 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 9999.970671818064986684 ETH
? Application address 0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e
? Input String encoding
```

### A entrada deverá ser uma string no formato json com da seguinte forma:
```
{"id":"<identificador de quem esta enviado o certificado>","publicKey":"<certificado contendo chave publica>,"signature":"<mensagem assinada pela chave privada>"}
```
A partir da entrada, o sistema verifica se o certificado com chave pública, enviado pelo identificador, foi gerado a partir da mesma chave privada que assinou a mensagem.

### Ações que podem ser realizadas a partir da entrada:
- *registrar uma nova chave pública por um usuário, com mensagem assinada*
- *alterar a chave pública e mensagem assinada registrada por um usuário*
- *Revogar uma chave pública registrada pelo usuário*
