import os
from datetime import datetime

class Cliente:
    def __init__(self, nome, senha, tipo_cliente="comum"):
        self.nome = nome
        self.senha = senha
        self.tipo_cliente = tipo_cliente
        self.saldo = 0.0
        self.historico = []
        self.saques_hoje = 0
        self.transferencias_hoje = 0
        self.ultimo_saque_dia = None
        self.ultima_transferencia_dia = None
        self.arquivo = f"{self.nome}.txt"

    def salvar_dados(self):
        with open(self.arquivo, 'w') as file:
            file.write(f"Nome: {self.nome}\n")
            file.write(f"Senha: {self.senha}\n")
            file.write(f"Tipo: {self.tipo_cliente}\n")
            file.write(f"Saldo: {self.saldo}\n")
            file.write(f"Saques Hoje: {self.saques_hoje}\n")
            file.write(f"Último Saque Dia: {self.ultimo_saque_dia}\n")
            file.write(f"Transferências Hoje: {self.transferencias_hoje}\n")
            file.write(f"Última Transferência Dia: {self.ultima_transferencia_dia}\n")
            file.write("Histórico de Operações:\n")
            for operacao in self.historico:
                file.write(operacao + "\n")

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as file:
                lines = file.readlines()
                self.saldo = float(lines[3].split(": ")[1])
                self.saques_hoje = int(lines[4].split(": ")[1])
                self.ultimo_saque_dia = lines[5].split(": ")[1].strip()
                self.transferencias_hoje = int(lines[6].split(": ")[1])
                self.ultima_transferencia_dia = lines[7].split(": ")[1].strip()
                self.historico = [line.strip() for line in lines[9:]]

    def atualizar_limites(self):
        hoje = datetime.now().strftime("%Y-%m-%d")
        if self.ultimo_saque_dia != hoje:
            self.saques_hoje = 0
            self.ultimo_saque_dia = hoje
        if self.ultima_transferencia_dia != hoje:
            self.transferencias_hoje = 0
            self.ultima_transferencia_dia = hoje

    def depositar(self, valor):
        self.saldo += valor
        self.historico.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Depósito de R$ {valor:.2f}")
        self.salvar_dados()

    def sacar(self, valor):
        self.atualizar_limites()
        if self.saques_hoje < 3:
            if valor <= self.saldo:
                self.saldo -= valor
                self.saques_hoje += 1
                self.historico.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Saque de R$ {valor:.2f}")
                self.salvar_dados()
            else:
                print("Saldo insuficiente.")
        else:
            print("Limite de 3 saques diários atingido.")

    def transferir(self, valor, destinatario):
        self.atualizar_limites()
        if self.transferencias_hoje < 10:
            if valor <= self.saldo:
                self.saldo -= valor
                destinatario.depositar(valor)
                self.transferencias_hoje += 1
                self.historico.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Transferência de R$ {valor:.2f} para {destinatario.nome}")
                self.salvar_dados()
                destinatario.salvar_dados()
            else:
                print("Saldo insuficiente.")
        else:
            print("Limite de 10 transferências diárias atingido.")

    def exibir_extrato(self, tipo_extrato="completo"):
        hoje = datetime.now().strftime("%Y-%m-%d")
        print("\nExtrato de Operações")
        print("-" * 40)
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("-" * 40)

        if tipo_extrato == "completo":
            for operacao in self.historico:
                print(operacao)
        elif tipo_extrato == "diario":
            operacoes_hoje = [op for op in self.historico if op.startswith(hoje)]
            for operacao in operacoes_hoje:
                print(operacao)
        
        print("-" * 40)


class DIOBank:
    def __init__(self):
        self.clientes = {}

    def criar_conta(self, nome, senha, tipo_cliente="comum"):
        if nome in self.clientes:
            print("Nome de usuário já existe.")
        else:
            cliente = Cliente(nome, senha, tipo_cliente)
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

    def buscar_cliente(self, nome):
        return self.clientes.get(nome, None)

    def listar_clientes(self):
        print("\nClientes cadastrados:")
        for cliente in self.clientes.values():
            print(f"Nome: {cliente.nome}, Tipo: {cliente.tipo_cliente}")

    def listar_contas(self):
        print("\nContas cadastradas:")
        for cliente in self.clientes.values():
            print(f"Cliente: {cliente.nome}, Saldo: R$ {cliente.saldo:.2f}")

    def acessar_menu_administrador(self):
        print("\n=== Menu de Administrador ===")
        while True:
            print("\n1. Listar todos os clientes")
            print("2. Listar todas as contas")
            print("3. Voltar")
            escolha = input("\nEscolha uma opção: ")

            if escolha == '1':
                self.listar_clientes()
            elif escolha == '2':
                self.listar_contas()
            elif escolha == '3':
                break
            else:
                print("Opção inválida.")


# Exemplo de uso do programa
def main():
    banco = DIOBank()

    while True:
        print("\n1. Criar conta")
        print("\n2. Logar")
        print("\n3. Acessar menu de administrador")
        print("\n4. Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            nome = input("Digite seu nome de usuário: ")
            senha = input("Digite sua senha: ")
            tipo_cliente = input("Digite o tipo de cliente (comum, premium): ")
            banco.criar_conta(nome, senha, tipo_cliente)

        elif escolha == '2':
            nome = input("Digite seu nome de usuário: ")
            senha = input("Digite sua senha: ")
            cliente = banco.logar(nome, senha)

            if cliente:
                while True:
                    print("\n1. Depositar")
                    print("\n2. Sacar")
                    print("\n3. Transferir")
                    print("\n4. Verificar extrato completo")
                    print("\n5. Verificar extrato do dia")
                    print("\n6. Sair")
                    escolha = input("\nEscolha uma opção: ")

                    if escolha == '1':
                        valor = float(input("Digite o valor para depósito: "))
                        cliente.depositar(valor)
                    elif escolha == '2':
                        valor = float(input("Digite o valor para saque: "))
                        cliente.sacar(valor)
                    elif escolha == '3':
                        destinatario_nome = input("Digite o nome do destinatário: ")
                        destinatario = banco.buscar_cliente(destinatario_nome)
                        if destinatario:
                            valor = float(input("Digite o valor para transferência: "))
                            cliente.transferir(valor, destinatario)
                        else:
                            print("Destinatário não encontrado.")
                    elif escolha == '4':
                        cliente.exibir_extrato(tipo_extrato="completo")
                    elif escolha == '5':
                        cliente.exibir_extrato(tipo_extrato="diario")
                    elif escolha == '6':
                        break
                    else:
                        print("Opção inválida.")

        elif escolha == '3':
            banco.acessar_menu_administrador()

        elif escolha == '4':
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

