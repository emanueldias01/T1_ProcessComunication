# login

print("1. Entrar")
print("2. Criar conta")

response = input("> ")

print("")
if response == "1":
    user = input("Usuário: ")
    password = input("Senha: ")

else:
    user = input("Usuário: ")
    password = input("Senha: ")
    password_confirm = input("Confirmar senha: ")


# enviar socket para login
## retorno {token de validação}
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("1. Mapas")
print("2. Mudar nome")
print("3. Deletar Conta")
print("4. Sair")

response = input()

# api/mapas/
print("nome      | tipo | numero_de_pessoas    | status | IP | Porta")
print("PixelHub \t padrão \t 2/10 \t online \t 127.0.0.1 \t 8888")



# se ADM criar board
## criar board, tipos

# se USER
## ler board