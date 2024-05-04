# MENU

menu = """"

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

# comando da operação

while True:
    opcao = input(menu)

# DEPOSITO

    if opcao == "1":
        valor= float (input ("Qual valor que deseja Depositar: "))

        if valor >= 1:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso.")
        
        else:
            print("Erro! Digite o valor maior que 0.")


# SACAR

    elif opcao == "2":
        valor = int (input ("Qual valor que deseja Sacar: "))

        execedeu_saldo = valor > saldo
        execedeu_limite = valor > limite
        execedeu_saques = numero_saque >= LIMITE_SAQUE

        
        if execedeu_saldo:
            print("Operação falhou! você não tem saldo suficiente.")

        elif execedeu_limite:
            print("Operação falhou! o valor do saque execedeu o limite")

        elif execedeu_saques:
            print("Operação falhou! Número maximo de saque execedido")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque += 1
            print("Saque realizado com sucesso.(;")

        else:
             print("Transição falhou!!")

      

# EXTRATO
    
    elif opcao == "3":
        print ("\n############### EXTRATO ###############")
        print ("Nã foram realizadas movimentações."if not extrato else extrato)
        print (f"\nSaldo: R$ {saldo:.2f}")
        print ("###### obrigado pela preferencia...######")


# SAIR

    elif opcao == "0":
        break

    else:
        print ("Operação invalida, por favor selecione selecione a operação desejada")    