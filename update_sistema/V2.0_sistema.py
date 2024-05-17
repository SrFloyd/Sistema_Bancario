from abc import ABC, abstractclassmethod, abstractproperty
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)    


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n Operação Falhou, Você Não Possui Saldo Suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque Realizado Com Sucesso. ===")
            return True
        
        else:
            print("\n Operação Falhou! O Valor Informado é Invalido.")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito Realizado Com Sucesso. ===")

        else:
            print("\n Operação Falhou! O Valor Informado é Invalido.")
            return False
        
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
            transacoes if transacao["tipo"] == Saque.
            __name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação Falhou! O Valor De Saque Excedeu o Limite.")

        elif excedeu_saques:
            print("\n Operação Falhou! Número maximo De Saques Excedido.")

        else:
            return super().sacar(valor)
        
        return False
    def __str__(self):
        return f"""\
            Agêcia:\t\t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transicao = conta.depositar(self.valor)
        
        if sucesso_transicao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """"
    ========= MENU =========
    
    [1]\t Depositar
    [2]\t Sacar
    [3]\t Extrato
    [4]\t Novo Usuário
    [5]\t Listar Contas
    [6]\t Nova Conta
    [0]\t Sair

    ========================
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in
    clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente Não possui Conta! ")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do Cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente Não Encontrado!")
        return
    
    valor = float(input("Digite o Valor do Depósito: "))
    Transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, Transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do Cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente Não Encontrado! ")
        return
    
    valor = float(input("Digite o Valor de Saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do Cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente: 
        print("\n Cliente Não Encontrado! ")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF(somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n Já Existe Cliente Com Esse CPF!")
        return
    
    nome = input("Digite Seu Nome Completo: ")
    data_nascimento = input("Digite Sua Data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o Indereço (logradouro, nro - bairro - cidade/sigla: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente Criado Com Sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do Cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente Não Encontrado, Fluxo de Criação de Conta Encerrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta Criada Com Sucesso!")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            listar_contas(contas)
        
        elif opcao == "6":
            numero_conta = len(contas) +1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "0":
            break

        else:
            print("\n Operação Invalida, Por Favor Selecione Novamente a Operação Desejada.")


main()