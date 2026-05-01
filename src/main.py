
from accounts import AccountStore
from cli import run_cli


def main():
	store = AccountStore()
	run_cli(store)


if __name__ == "__main__":
	main()