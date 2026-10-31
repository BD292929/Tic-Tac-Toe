import csv
import os
import pickle
from Class_Game import *

class Tournament:
    def __init__(self, game: Game, csv_results='results.csv', csv_monte_carlo = 'monte_carlo.csv', csv_monte_carlo_pkl = 'monte_carlo_pkl.csv'):
        self.game = game #שומר אובייקט של Game
        self.csv_results = csv_results #זוכר את הcsv
        self.csv_monte_carlo = csv_monte_carlo
        self.csv_monte_carlo_pkl = csv_monte_carlo_pkl
        self.wins = 0 #סופר ניצחונות
        self.losses = 0 #סופר הפסדים 
        self.draws = 0 #סופר תיקואים
        self.headers = ['(0,0)','(1,0)','(2,0)','(0,1)','(1,1)','(2,1)','(0,2)','(1,2)','(2,2)','result'] #זוכר את הכותרות של הcsv 
        self.score = {}

        #מנתב את הקבצים להווצר בתיקייה של האיקס עיגול
        base_dir = base_dir = r"C:\Users\keren\Downloads\למידת מכונה\משחק איקס עיגול"
        self.csv_results = os.path.join(base_dir, csv_results)
        self.csv_monte_carlo = os.path.join(base_dir, csv_monte_carlo)
        self.csv_monte_carlo_pkl = os.path.join(base_dir, csv_monte_carlo_pkl)

    def board_to_arr(self, board):
        mapping = {'x': 1, 'o': -1, ' ': 0}  #עושה מילון של ערכים לכל פרמטר שעל הלוח
        arr = [] #מערך שאליו אני מכניס את הלוח שלי על פי הפרמטרים
        positions_order = [(0, 0),(1, 0),(2, 0),(0, 1),(1, 1),(2, 1),(0, 2),(1, 2),(2, 2)] #מערך שעוזר לי להכניס את הערכים למיקומם הנכון
        for r, c in positions_order: #לולאת פור שמכניס על את הערכים על פי המיקום שלהם r וc הם המיקומים
            arr.append(mapping[board[r][c]]) #הפעולה שמכניסה לתוך המערך את הערכים למיקום הנכון
        return arr #מחזיר את המערך מסודר

    def play_games(self, count): #הפונקציה שמריצה לי את כל המשחקים (מקבלת כמה משחקים להריץ)
        file_exists = os.path.exists(self.csv_results) #בודק אם הקובץ כבר קיים

        with open(self.csv_results, mode='a', newline='', encoding='utf-8') as f: #פתיחת הקובץ
            writer = csv.writer(f) #מאפשר הזרקה של שורות נתונים מפייתון ישר לקובץ csv

            #בודק אם הקובץ כבר קיים ואם הוא לא קיים אז מוסיף לו את הכותרת 
            if not file_exists:
                writer.writerow(self.headers)


            for i in range(1,count+1): #מריץ count משחקים
                boards, final_board, result = self.game.play() #מריץ את המשחק מהלוח ממקבל תוצאה ולוח סופי

                for board in boards:
                    key = tuple(tuple(row) for row in board[0])

                    if key in self.score: 
                        self.score[key][0] += board[1]
                        self.score[key][1] += 1
                    else:
                        self.score[key] = [board[1], 1]

                #בודק אם יש ניצחון, הפסד או תיקו
                if result == 1:
                    self.wins += 1
                elif result == -1:
                    self.losses += 1
                elif result == 0:
                    self.draws += 1

                row_data = self.board_to_arr(final_board) #הופך את הלוח למערך חד מימדי ושם בdata
                #אם זה תיקו התוצאה תהיה 2
                if(result == 0):
                    row_data.append(2)
                else:
                    row_data.append(result) 
                writer.writerow(row_data) #מוסיף את הלוח והתוצאה לשורה בקובץ

                #מדפיס כל מאה משחקים כמה משחקים הרצנו
                if i % 100 == 0:
                    print(f"הושלמו {i}/{count} משחקים... (ניצחונות: {self.wins}, הפסדים: {self.losses}, תיקו: {self.draws})")

            self.print_tournament_results() #קוראת לפונקציה שמדפיסה את התוצאות של הטורניר

            self.score_to_scv()

    def score_to_scv(self):

        #עושה מילון עם ניקוד ממוצע
        average_scores = {}

        for board, (score, count) in self.score.items():
            average_scores[board] = [score/count, count]

        #שמירה כ-pickle
        with open(self.csv_monte_carlo_pkl, 'wb') as f:
            pickle.dump(average_scores, f)

        #שמירה כ-csv
        with open(self.csv_monte_carlo, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Board', 'Average Score', 'Board Count'])

            for board, (score, count) in average_scores.items():
                writer.writerow([board, score, count])
    
    def print_tournament_results(self):

            print('=== סיכום הטורניר ===') #מדפיס כותר סיום
            print(f'ניצחונות (X): {self.wins}') #מדפיס את מספר הניצחונות
            print(f'הפסדים (O): {self.losses}') #מדפיס את מדפיס ההפסדים
            print(f'תיקו: {self.draws}') #מדפיס את מספר התיקואים

    #פונקציות שמחזירות את מספר הניצחונות, הפסדרים ותיקואים
    def win(self):
        return self.wins
    def losse(self):
            return self.losses
    def draw(self):
            return self.draws