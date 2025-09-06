from customtkinter import *
from preprocessing import clean
from load import loader, getArticle
from datetime import datetime
import json
import csv
import webbrowser
from dataManager import submit, remove, find, FILE, INFO_FILE

import threading
from api_server import run_api

title_mod, text_mod, config = loader()

BG_COLOR = "#0f172a"
PRIMARY_COLOR = "#334155"
SECONDARY_COLOR = "#9ca4b3"

WINDOW_SIZE = 600

class App(CTk):
    def __init__(self):
        threading.Thread(target=run_api, daemon=True).start()

        super().__init__()

        self.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        self.title("Tru")
        self.configure(background=BG_COLOR)

        self.pages = {}

        for Page in (MainPage, HistoryPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            frame.configure(fg_color=BG_COLOR)
            self.pages[page_name] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_page("MainPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


class MainPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.currTitleScore = 0
        self.currTextScore = 0
        self.currWeightedScore = 0

        CTkLabel(self, text="Bias Breaker", text_color="white", font=("Arial", 22)).pack(pady=20)

        self.urlEntry = CTkEntry(self,
                                 width=400,
                                 bg_color=PRIMARY_COLOR,
                                 text_color=SECONDARY_COLOR,
                                 fg_color="transparent",
                                 border_width=2,
                                 placeholder_text="Enter URL...")
        self.urlEntry.place(x=100, y=100)

        CTkButton(self,
                  text="Submit",
                  command=self.getInfo,
                  corner_radius=25).place(x=230, y=150)

        self.result = CTkFrame(self,
                               fg_color=PRIMARY_COLOR,
                               border_width=5,
                               width=300, height=150)
        self.result.pack_propagate(False)

        self.resultTitle = CTkLabel(self.result, text="Results", text_color=SECONDARY_COLOR, font=("Arial", 16, "bold"))
        self.resultTitle.pack(pady=(5, 2))

        self.titleScoreLab = CTkLabel(self.result, text_color=SECONDARY_COLOR)
        self.titleScoreLab.pack(pady=2)

        self.textScoreLab = CTkLabel(self.result, text_color=SECONDARY_COLOR)
        self.textScoreLab.pack(pady=2)

        self.weightedScoreLab = CTkLabel(self.result, text_color=SECONDARY_COLOR)
        self.weightedScoreLab.pack(pady=(2, 5))

        CTkButton(self, text="Go to History", command=lambda: controller.show_page("HistoryPage")).place(x=240, y=540)

    def getInfo(self):
        title, text = getArticle(self.urlEntry.get(), config)

        if not title or not title.strip():
            print("Invalid URL")
            return

        self.currTitleScore = title_mod.predict_proba([title])[0][0]
        self.currTextScore = text_mod.predict_proba([text])[0][0]
        self.currWeightedScore = (0.8 * self.currTextScore) + (0.2 * self.currTitleScore)

        resultBool = self.currWeightedScore < 0.75

        self.titleScoreLab.configure(text=f"Title Score: {self.currTitleScore:.4f}")
        self.textScoreLab.configure(text=f"Text Score: {self.currTextScore:.4f}")
        self.weightedScoreLab.configure(text=f"Weighted Score: {self.currWeightedScore:.4f}")

        self.result.place(x=(WINDOW_SIZE / 2 - 150), y=360)

        with open(INFO_FILE, 'r') as file:
            info = json.load(file)

        row = [info.get("idNum"),
               datetime.now().date(),
               title,
               self.currWeightedScore,
               resultBool,
               self.urlEntry.get()]

        submit(row)


class HistoryPage(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        CTkLabel(self, text="History Page", text_color="white", font=("Arial", 22)).pack(pady=20)

        self.scroll = CTkScrollableFrame(self, width=500, height=400)
        self.scroll.pack(pady=10, padx=20)

        self.populate_history()

        CTkButton(self, text="Back to Main", command=lambda: controller.show_page("MainPage")).place(x=240, y=540)

    def make_label_clickable(self, label, url):
        def callback(event):
            webbrowser.open(url)
        label.bind("<Button-1>", callback)
        label.configure(cursor="hand2")

    def populate_history(self):
        try:
            with open(FILE, "r") as f:
                reader = csv.reader(f)
                next(reader)
                rows = list(reader)[-20:]

            for row in reversed(rows):
                date, title, score, is_real, url = row[1], row[2], float(row[3]), row[4], row[5]
                text = f"[{date}]  {title} — Score: {score:.2f}  — {'REAL' if is_real == 'True' else 'FAKE'}"
                label = CTkLabel(self.scroll, text=text, text_color="#d1d5db", wraplength=480, justify="left")
                label.pack(anchor="w", pady=5)

                self.make_label_clickable(label, url)

        except Exception as e:
            CTkLabel(self.scroll, text=f"Error loading history: {e}", text_color="red").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
