from sys import argv

TOKEN_FILE_PATH = "permanent_storage/test_token.dat"

if __name__ == "__main__":
    with open(TOKEN_FILE_PATH, "w") as token_file:
        token_file.write(argv[1])
