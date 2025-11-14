# app/core/security.py
import bcrypt


def get_password_hash(password: str) -> str:

    try:
        pwd_context = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        return pwd_context.decode('utf-8')
    
    except Exception as e:
        print("Error occurred while hashing password:", e)
        raise

def verify_password(plain: str, hashed: str) -> bool:

    try:
        hashed_bytes = hashed.encode("utf-8")

        # return bcrypt.checkpw(plain, hashed)
        return bcrypt.checkpw(plain.encode("utf-8"), hashed_bytes)

    except Exception as e:
        print("Error occurred while verifying password:", e)
        raise
