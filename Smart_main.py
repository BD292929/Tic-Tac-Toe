from Class_Game import *
from Class_Smart_tournament import *

if __name__ == "__main__":
    
    game = Game() #יצירת אובייקט Game
    smart_tournament = Smart_tournemnt(game) #יצירת אובייקט Tournament

    rounds = input("How many rounds?")

    print(f"מתחיל טורניר של {rounds} משחקים...")
    print("-" * 34)

    smart_tournament.smart_play_games(int(rounds))

    print('---- אחוזים ----')
    total_rounds = float(rounds)
    
    print(f'ניצחונות (X): {((smart_tournament.win()) / total_rounds) * 100}%') 
    print(f'הפסדים (O): {((smart_tournament.losse()) / total_rounds) * 100}%') 
    print(f'תיקו: {((smart_tournament.draw()) / total_rounds) * 100}%') 
    