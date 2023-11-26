from PIL import Image
from tkinter import Tk, filedialog

def select_file(title, filetypes):
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def select_text():
    text = input("Enter the text: ")
    return text

def select_key():
    key = input("Enter the encryption/decryption key: ")
    return key

def select_output_path(action):
    root = Tk()
    root.withdraw()  # Hide the main window
    output_path = filedialog.asksaveasfilename(
        title=f"Select a path to save the {action} image",
        defaultextension=".png",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    return output_path

def xor_crypt(text, key):
    # XOR encryption and decryption are the same for a simple XOR cipher
    return ''.join(chr(ord(char) ^ ord(key_char)) for char, key_char in zip(text, key))

def encode_image(image_path, message, key, output_path):
    encrypted_message = xor_crypt(message, key)
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message)

    data_index = 0
    img = Image.open(image_path)
    img_data = list(img.getdata())

    for i in range(len(img_data)):
        pixel = list(img_data[i])
        for j in range(3):  # RGB channels
            if data_index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[data_index])
                data_index += 1
        img_data[i] = tuple(pixel)

    encoded_img = Image.new('RGB', img.size)
    encoded_img.putdata(img_data)
    encoded_img.save(output_path)

def decode_image(image_path, key):
    img_data = list(Image.open(image_path).getdata())
    binary_message = ''.join(bin(value)[-1] for pixel in img_data for value in pixel)
    decrypted_message = xor_crypt(''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)), key)
    return decrypted_message

def main():
    while True:
        print("\nSteganography Tool")
        print("------------------")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. End")

        # Choose action
        choice = input("Enter choice (1, 2, or 3): ")

        if choice == "1":
            image_path = select_file("Select an image file", [("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            text = select_text()
            key = select_key()
            output_path = select_output_path("encrypted")
            encode_image(image_path, text, key, output_path)
            print(f"Text encrypted and encoded. Encrypted image saved to {output_path}")

        elif choice == "2":
            image_path = select_file("Select an image file", [("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            key = select_key()
            decrypted_message = decode_image(image_path, key)
            print("Decrypted Message:", decrypted_message)

        elif choice == "3":
            print("Exiting the Steganography Tool.")
            break

        else:
            print("Invalid choice. Please enter '1' for encryption, '2' for decryption, or '3' to end.")

if __name__ == "__main__":
    main()
