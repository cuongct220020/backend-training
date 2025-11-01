# app/misc/generate_secret_key.py
import secrets

if __name__ == "__main__":
    # Tạo một key ngẫu nhiên 32-byte (tương đương 256-bit)
    # Đây là độ dài an toàn và được khuyến nghị cho thuật toán HS256.
    secret_key = secrets.token_hex(32)

    print("=" * 50)
    print("🔑 Your new secret key is:")
    print(f"\n{secret_key}\n")
    print("=" * 50)
    print("ACTION: Copy this key and paste it into your .env file.")
    print("Example: JWT_SECRET=\"<your_key_here>\"")
    print("=" * 50)
