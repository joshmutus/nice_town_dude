from nice_town_dude.game_view import GameView
import arcade

def main():
    """Main function"""
    window = GameView()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()