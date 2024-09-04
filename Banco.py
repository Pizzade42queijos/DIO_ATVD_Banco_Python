import os

class Cliente:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha
        self.saldo = 0.0
        self.historico = []
        self.arquivo = f"Data.txt"

    def salvar_dados(self):
        with open(self.arquivo, 'w') as file:
            file.write(f"Nome: {self.nome}\n")
            file.write(f"Senha: {self.senha}\n")
            file.write(f"Saldo: {self.saldo}\n")
            file.write("Histórico de Operações:\n")
            for operacao in self.historico:
                file.write(operacao + "\n")

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as file:
                lines = file.readlines()
                self.saldo = float(lines[2].split(": ")[1])
                self.historico = [line.strip() for line in lines[4:]]

    def depositar(self, valor):
        self.saldo += valor
        self.historico.append(f"Depósito de R$ {valor:.2f}")
        self.salvar_dados()

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            self.historico.append(f"Saque de R$ {valor:.2f}")
            self.salvar_dados()
        else:
            print("Saldo insuficiente.")

    def exibir_extrato(self):
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("Histórico de Operações:")
        for operacao in self.historico:
            print(operacao)


class DIOBank:
    def __init__(self):
        self.clientes = {}

    def criar_conta(self, nome, senha):
        if nome in self.clientes:
            print("Nome de usuário já existe.")
        else:
            cliente = Cliente(nome, senha)
            self.clientes[nome] = cliente
            cliente.salvar_dados()
            print(f"Conta criada para {nome}.")

    def logar(self, nome, senha):
        if nome in self.clientes:
            cliente = self.clientes[nome]
            cliente.carregar_dados()
            if cliente.senha == senha:
                print(f"Bem-vindo, {nome}!")
                return cliente
            else:
                print("Senha incorreta.")
        else:
            print("Conta não encontrada.")
        return None


# Exemplo de uso do programa
def main():
    banco = DIOBank()

    while True:
        print("\n1. Criar conta")
        print("\n2. Logar")
        print("\n3. Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            nome = input("Digite seu nome de usuário: ")
            senha = input("Digite sua senha: ")
            banco.criar_conta(nome, senha)

        elif escolha == '2':
            nome = input("Digite seu nome de usuário: ")
            senha = input("Digite sua senha: ")
            cliente = banco.logar(nome, senha)

            if cliente:
                while True:
                    print("\n1. Depositar")
                    print("\n2. Sacar")
                    print("\n3. Verificar extrato")
                    print("\n4. Sair")
                    escolha = input("\nEscolha uma opção: ")

                    if escolha == '1':
                        valor = float(input("Digite o valor para depósito: "))
                        cliente.depositar(valor)
                    elif escolha == '2':
                        valor = float(input("Digite o valor para saque: "))
                        cliente.sacar(valor)
                    elif escolha == '3':
                        cliente.exibir_extrato()
                    elif escolha == '4':
                        break
                    else:
                        print("Opção inválida.")

        elif escolha == '3':
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
