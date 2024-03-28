from passlib.context import CryptContext


class PasswordMaker:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def get_password_hash(password: str) -> str:
        return PasswordMaker.pwd_context.hash(password)
    
    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        return PasswordMaker.pwd_context.verify(password, hashed_password)


if __name__ == "__main__":
    print(PasswordMaker.get_password_hash(r'guestguestguestguestguestguest#%!'))