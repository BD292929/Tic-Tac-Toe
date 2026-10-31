import random
import copy
import pickle
#from Class_Monte_Carlo import *

class Game:
    def __init__(self, size=3):
        self.size = size

        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)] #יוצר את  מטריצה שהיא בעצם הלוח שלנו בגודל size x size
        self.available_positions = [(i, j) for i in range(self.size) for j in range(self.size)]  #יוצר רשימה של מקומות פנויים על הלוח

        with open(r"C:\Users\keren\Downloads\למידת מכונה\משחק איקס עיגול\monte_carlo_pkl.csv", 'rb') as f:
            self.scores = pickle.load(f)

    def perform_agent_move(self): 
        p = random.randint(0, len(self.available_positions) - 1) #מגריל מיקום רנדומלי שפנוי על הלוח
        row, col = self.available_positions.pop(p) #מוציא את המיקום המוגרל מהמערך של המקומות הפנויים
        
        self.board[row][col] = "x" # שם איקס במיקום שהוגרל

    def preform_best_move(self):

        best_score = -1.0
        best_position = None

        for r, c in self.available_positions:

            temp_board = copy.deepcopy(self.board)
            temp_board[r][c] = "x"

            key = tuple(tuple(row) for row in temp_board)

            if key in self.scores:
                avg_score, count = self.scores[key]

                if avg_score > best_score:
                    best_score = avg_score
                    best_position = (r, c)

        if best_position is None:
            best_position = random.choice(self.available_positions)

        r, c = best_position

        self.available_positions.remove(best_position)
        self.board[r][c] = "x"
    
    def perform_rival_move(self):
        p = random.randint(0, len(self.available_positions) - 1) #מגריל מיקום רנדומלי שפנוי על הלוח
        row, col = self.available_positions.pop(p) #מוציא את המיקום המוגרל מהמערך של המקומות הפנויים
    
        self.board[row][col] = "o" # שם עיגול במיקום שהוגרל

    def check_win(self):
        for player, score in [("x", 1), ("o", -1)]: #נותן ערכים לאיקס ולעיגול

            #בודק אם יש שורה שהיא שווה בערכים
            for row in self.board:
                if all(cell == player for cell in row):
                    return score

            #בודק אם יש עמודה שהיא שווה בערכים
            for col in range(self.size):
                if all(self.board[row][col] == player for row in range(self.size)):
                    return score

            # 3. בדיקת אלכסון ראשי
            if all(self.board[i][i] == player for i in range(self.size)):
                return score

            # 4. בדיקת אלכסון משני
            if all(self.board[i][self.size - 1 - i] == player for i in range(self.size)):
                return score

        if not self.available_positions: #בודק אם יש מקומות פנויים בלוח
            return 0
        
        return 2 #אם אף אחד לא ניצח והלוח לא מלא אז ממשיכים לשחק

    def print_game_result(self):
        if(self.check_win() == -1): #בודק אם עיגול ניצח 
            print("o won")
        elif(self.check_win() == 1): #בודק אם איקס ניצח
            print("x won")
        elif(self.check_win() == 0): #בודק אם יש תיקו
            print("draw")
        
    def print_board(self):
        cols_header = "    " + "   ".join(str(j) for j in range(self.size)) #יוצר את הכותרות(מספורים) של העמודות בגודל של size
        print(cols_header)
    
        separator = "  " + "-" * (self.size * 4 + 1) # כותב את הרצפה/תקרה של השורה לפי נוסחא שתתאים לגודל של size
        print(separator)

        for i in range(self.size):
            row_str = f"{i} | " + " | ".join(self.board[i]) + " |" #כותב את המצב של הלוח עם הפרדה יפה של המקומות שבלוח
            print(row_str)
            print(separator)

    def cleanboard(self):
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)] #יוצר את  מטריצה שהיא בעצם הלוח שלנו בגודל size x size והיא ריקה
        self.available_positions = [(i, j) for i in range(self.size) for j in range(self.size)]  #יוצר רשימה של מקומות פנויים על הלוח

    def give_score(self, list, num):
        scored_boards = []

        for board in reversed(list):
            scored_boards.append((board, num))
            num = num * 0.8

        return scored_boards

    def play(self):
        self.cleanboard() #מנקה את הלוח לפני כל משחק חדש

        boards = []

        while(self.check_win() == 2):

            '''---מונטה קארלו משלי---'''
            #mc = Monte_Carlo(self) #יוצר אובייקט מונטה קארלו
            #mc.run_simulations() #מריץ מונטה קארלו על הלוח שיש לנו עכשיו

            #עושה אותו חכם
            # best_pos = mc.get_best_move() #מקבל את המהלך הכי טוב לעשות מהמונטה קארלו

            # self.board[best_pos[0]][best_pos[1]] = 'x' #עושה את המהלך שקיבל את הציון הכי גבוהה במונטה קארלו
            # self.available_positions.remove(best_pos) #מוריד את המיקום הכי טוב מהלוח כי עשינו אותו
            '''---מונטה קארלו משלי---'''

            self.perform_agent_move()
            boards.append(copy.deepcopy(self.board))
            #בודק אם יש ניצחון ואם כן יוצא מהלולאה
            if(self.check_win() != 2):
                break

            self.perform_rival_move() #היריב עושה תור
            boards.append(copy.deepcopy(self.board))

        if(self.check_win() == 1):
            boards = self.give_score(boards, 1.0)
        elif(self.check_win() == -1):
            boards = self.give_score(boards, 0.0)
        else:
            boards = self.give_score(boards, 0.2)

        return boards, self.board, self.check_win() #מחזיר את הלוח ומי ניצח  וישמש בהמשך ליצירת  הקובץ csv שאותו אני מייצר במחלקה Tournament

    def smart_paly(self):
        self.cleanboard() #מנקה את הלוח לפני כל משחק חדש

        boards = []
        
        while(self.check_win() == 2):

            self.preform_best_move()
            boards.append(copy.deepcopy(self.board))
            #בודק אם יש ניצחון ואם כן יוצא מהלולאה
            if(self.check_win() != 2):
                break

            self.perform_rival_move() #היריב עושה תור
            boards.append(copy.deepcopy(self.board))

        if(self.check_win() == 1):
            boards = self.give_score(boards, 1.0)
        elif(self.check_win() == -1):
            boards = self.give_score(boards, 0.0)
        else:
            boards = self.give_score(boards, 0.2)

        return boards, self.board, self.check_win() #מחזיר את הלוח ומי ניצח  וישמש בהמשך ליצירת  הקובץ csv שאותו אני מייצר במחלקה Tournament