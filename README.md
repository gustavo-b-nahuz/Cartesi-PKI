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

### Para iniciar o Cartesi (Manter este terminal aberto e utilizar outro para os próximos passos):
```bash
cartesi run
```

### Para utilizar o Advance no Cartesi:

#### Comando para enviar entradas genéricas para a aplicação (Em um novo terminal):
```bash
cartesi send generic
```

#### Teclar Enter até o momento de Input String
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

#### A entrada deverá ser uma string no formato json com da seguinte forma:
```
{"id":"<identificador de quem esta enviado o certificado>","publicKey":"<certificado contendo chave publica>,"signature":"<mensagem assinada pela chave privada>"}
```
A partir da entrada, o sistema verifica se o certificado com chave pública percente ao identificador a partir da assinatura, ou seja, se foi gerado a partir da mesma chave privada que assinou a mensagem.

#### Ações que podem ser realizadas a partir da entrada:
- *registrar uma nova chave pública por um usuário, com mensagem assinada*;
  - Caso o usuário não possua nenhuma chave pública registrada e a mesma tenha sido validada pela assinatura, a chave pública é registrada.
- *alterar a chave pública e mensagem assinada registrada por um usuário*;
  - Caso o usuário possua uma chave pública registrada e envie uma nova, que tenha sido validada pela assinatura, a chave pública é alterada.
- *Revogar uma chave pública registrada pelo usuário*.
  - Caso o usuário envie a mesma chave pública que está registrada atualmente, validada pela assinatura, a chave pública é revogada.
 
### Para verificar o estados da Blockchain:
É mostrado um array de estados, onde o último mostrado é o atual.

### Para utilizar o Inspect no Cartesi:

