import textwrap

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

def depositar(saldo, valor , extrato, /):
    if valor >= 1:
         saldo += valor
         extrato += f"Depósito:\t R$ {valor:.2f}\n"
         print("Depósito realizado com sucesso.")
        
    else:
        print("Erro! Digite o valor maior que 0.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saque, limite_saque):
    execedeu_saldo = valor > saldo
    execedeu_limite = valor > limite
    execedeu_saques = numero_saque >= limite_saque
        
    if execedeu_saldo:
        print("Operação falhou! você não tem saldo suficiente.")

    elif execedeu_limite:
        print("Operação falhou! o valor do saque execedeu o limite")

    elif execedeu_saques:
        print("Operação falhou! Número maximo de saque execedido")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t \t R$ {valor:.2f}\n"
        numero_saque += 1
        print("Saque realizado com sucesso.(;")

    else:
         print("Transição falhou!!")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print ("\n=============== EXTRATO ===============")
    print ("Não foram realizadas movimentações."if not extrato else extrato)
    print (f"\nSaldo: R$ {saldo:.2f}")
    print ("======obrigado pela preferencia...======")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nUsuário com esse CPF já existente!")
        return
    
    nome = input("Digite seu nome completo: ")
    data_nascimento = input("Digite a data de nascimento (Dia-Mês-Ano): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append ({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios) 

    if usuario:
        print("\n === Conta criada com sucesso!===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n Usuário não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saque = 0
    usuarios = []
    contas = []
#   #contador_de_contas = 1

    while True:
        opcao = menu()

        if opcao == "1":
            valor= float (input ("Qual valor que deseja Depositar: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input ("Qual valor que deseja Sacar: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saque=numero_saque,
                limite_saque=LIMITE_SAQUE,
            )
 
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
#               #contador_de_contas += 1

        elif opcao == "0":
            break

        else:
            print ("Operação invalida, por favor selecione selecione a operação desejada")  

main()  
