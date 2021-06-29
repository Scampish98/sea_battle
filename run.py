from player import AI, Player


def main():
    ai = AI()
    ai.build_field()

    player = Player()
    player.build_field()

    players = [player, ai]
    current_player = 0
    while True:
        print("\nВаше текущее поле:")
        player.print_field()
        print("Текущее поле противника:")
        ai.print_hidden_field()
        if not players[current_player].hit(players[current_player ^ 1]):
            current_player ^= 1
        elif not players[current_player ^ 1].check_alive_ships():
            print()
            print("Победа!" if players[current_player] == player else "Поражение!")
            break

    print("Ваше итоговое поле:")
    player.print_field()
    print("Итоговое поле противника:")
    ai.print_field()


if __name__ == "__main__":
    main()
