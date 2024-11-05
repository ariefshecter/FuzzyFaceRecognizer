from register import register
from attendance import attendance

# Menu utama
def main():
    while True:
        print("\nMenu:")
        print("1. Registrasi")
        print("2. Absen")
        print("3. Keluar")

        choice = input("Pilih menu: ")
        if choice == '1':
            register()
        elif choice == '2':
            attendance()
        elif choice == '3':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
