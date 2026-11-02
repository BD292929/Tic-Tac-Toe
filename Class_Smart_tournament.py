import csv
import os
from Class_Game import *

class Smart_tournemnt:
    def __init__(self, game: Game, smart_results='smart_results.csv'):
        self.game = game
        self.smart_results = smart_results
        self.draws = 0
        self.wins = 0
        self.losses = 0
        self.games_count = 0
        

    def smart_play_games(self,count):
            
        for i in range(1,count+1): #מריץ count משחקים
            boards, final_board, result = self.game.smart_paly() #מריץ את המשחק מהלוח ממקבל תוצאה ולוח סופי

            if result == 1:
                self.wins += 1
            elif result == -1:
                self.losses += 1
            elif result == 0:
                self.draws += 1

            self.games_count +=1

            #מדפיס כל מאה משחקים כמה משחקים הרצנו
            if i % 100 == 0:
                print(f"הושלמו {i}/{count} משחקים... (ניצחונות: {self.wins}, הפסדים: {self.losses}, תיקו: {self.draws})")

        self.save_csv()

    def save_csv(self):
        file_exists = os.path.exists(self.smart_results) #בודק אם הקובץ כבר קיים

        with open(self.smart_results, mode='a', newline='', encoding='utf-8') as f: #פתיחת הקובץ
            writer = csv.writer(f) #מאפשר הזרקה של שורות נתונים מפייתון ישר לקובץ csv
        
                    #בודק אם הקובץ כבר קיים ואם הוא לא קיים אז מוסיף לו את הכותרת 
            if not file_exists:
                writer.writerow(['gamma','draw','loose','win_precent','draw_precent','loose_precent'])

            win_percent = self.wins / self.games_count * 100
            draw_percent = self.draws / self.games_count * 100
            loose_percent = self.losses / self.games_count * 100

            writer.writerow([0.75, 0.2, 0.0, win_percent, draw_percent, loose_percent])
            
    #פונקציות שמחזירות את מספר הניצחונות, הפסדרים ותיקואים
    def win(self):
        return self.wins
    def losse(self):
            return self.losses
    def draw(self):
            return self.draws
    