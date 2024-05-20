from app.api.src.switch_bot import SwitchBot


def main():
    switch_bot = SwitchBot()
    print(switch_bot.get_device_list())


if __name__ == "__main__":
    main()
