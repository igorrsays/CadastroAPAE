import login
import PythonApplication1

def main():
    if login.show_login():
        PythonApplication1.main()
    else:
        print("Login falhou ou foi cancelado.")

if __name__ == "__main__":
    main()
