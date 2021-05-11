import os

class App:
    global title
    title = "Twitch Bot Menu"

    def bot():
        print("OOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OOOOOOOOOOOOOOO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OO           OO  OO            OO               OO")
        print("OOOOOOOOOOOOOOO  OOOOOOOOOOOOOOOO               OO")

    def selectUser():
        print("\n")
        print(title)
        print("Qual o nome de usuário?")
        print()

    def items():
        print("\n")
        print(title)
        print("1. Criar contas")
        print("2. Ganhar seguidores")
        print("3. Ganhar views")
        print("4. Sair")
        print()

    def createAccounts():
        print("\n")
        print(title)
        print("4. Sair")
        print()

    def consoleClear():
        if os.name == "nt":
            os.system("clear")
        else:
            os.system("cls")