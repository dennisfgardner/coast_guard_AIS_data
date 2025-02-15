"main entry point"

from pprint import pprint

from marine_cadastre.config import Config


def main():
    print("Running Marine Cadastre Main Function")
    config = Config()
    pprint(config)


if __name__ == "__main__":
    main()
