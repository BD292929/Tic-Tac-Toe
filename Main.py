from Class_Tournament import *

if __name__ == "__main__":

    game = Game() #יצירת אובייקט Game
    tournament = Tournament(game) #יצירת אובייקט Tournament

    rounds = input("How many rounds?")
    
    print(f"מתחיל טורניר של {rounds} משחקים...")
    print("-" * 34)
        
    tournament.play_games(int(rounds))
    
    print('---- אחוזים ----')
    total_rounds = float(rounds)
            
    print(f'ניצחונות (X): {((tournament.win()) / total_rounds) * 100}%') 
    #print(f'הפסדים (O): {((tournament.losse()) / total_rounds) * 100}%') 
    #print(f'תיקו: {((tournament.draw()) / total_rounds) * 100}%') 
