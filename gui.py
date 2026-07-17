
import tkinter as tk
from tkinter import ttk, messagebox
from core.ranking_engine import RankingEngine
from core.portfolio_engine import PortfolioEngine

class RoboAdvisorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Robo Advisor")
        self.geometry("820x560")
        self.resizable(False, False)

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Capitale (€):").pack(side="left")
        self.capital = tk.StringVar(value="4000")
        ttk.Entry(top, textvariable=self.capital, width=12).pack(side="left", padx=5)
        ttk.Button(top, text="Aggiorna", command=self.refresh).pack(side="left", padx=10)
        ttk.Button(top, text="Ribilancia", command=self.rebalance).pack(side="left")
        ttk.Button(top, text="Esci", command=self.destroy).pack(side="right")

        body = ttk.Frame(self, padding=10)
        body.pack(fill="both", expand=True)

        left = ttk.LabelFrame(body, text="Ranking AI")
        left.pack(side="left", fill="both", expand=True, padx=(0,5))

        self.rank = ttk.Treeview(left, columns=("score",), show="headings", height=18)
        self.rank.heading("score", text="Score")
        self.rank.column("score", width=80, anchor="center")
        self.rank["displaycolumns"]=("score",)
        self.rank.pack(fill="both", expand=True)

        # use iid as symbol and show symbol in first column #0
        self.rank["show"]="tree headings"
        self.rank.heading("#0", text="ETF")
        self.rank.column("#0", width=120)

        right = ttk.LabelFrame(body, text="Portafoglio")
        right.pack(side="left", fill="both", expand=True)

        cols=("peso","importo","quote")
        self.port = ttk.Treeview(right, columns=cols, show="tree headings", height=18)
        self.port.heading("#0", text="ETF")
        self.port.column("#0", width=100)
        for c,t,w in zip(cols,["Peso %","Importo","Quote"],[70,90,90]):
            self.port.heading(c,text=t)
            self.port.column(c,width=w,anchor="center")
        self.port.pack(fill="both", expand=True)

        self.status=tk.StringVar(value="Pronto")
        ttk.Label(self,textvariable=self.status,relief="sunken",anchor="w").pack(fill="x",side="bottom")
        self.refresh()

    def refresh(self):
        try:
            cap=float(self.capital.get())
        except ValueError:
            messagebox.showerror("Errore","Capitale non valido")
            return

        for i in self.rank.get_children():
            self.rank.delete(i)
        for i in self.port.get_children():
            self.port.delete(i)

        ranking=RankingEngine()
        portfolio=PortfolioEngine(cap)

        try:
            data=ranking.top(10)
            for r in data:
                self.rank.insert("", "end", iid=r["symbol"], text=r["symbol"], values=(f'{r["score"]:.1f}',))

            p=portfolio.build()
            portfolio.save(p, "portfolio/target_portfolio.json")
            for x in p:
                self.port.insert("", "end", text=x["symbol"],
                    values=(f'{x["weight"]:.2f}',
                            f'€ {x["amount"]:.2f}',
                            f'{x["shares"]:.4f}'))
        finally:
            ranking.close()
            portfolio.close()

        self.status.set(f"Portafoglio aggiornato - Capitale € {cap:,.2f}")

    def rebalance(self):
        messagebox.showinfo("Rebalance","Usa app.py oppure integra il RebalanceEngine nel prossimo passo.")

if __name__=="__main__":
    RoboAdvisorGUI().mainloop()
