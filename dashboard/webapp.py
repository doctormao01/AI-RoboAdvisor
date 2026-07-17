from flask import Flask, render_template
from core.ranking_engine import RankingEngine
from core.portfolio_engine import PortfolioEngine

app=Flask(__name__)

@app.route("/")
def index():
    r=RankingEngine()
    p=PortfolioEngine(4000)
    try:
        ranking=r.top(10)
        portfolio=p.build()
    finally:
        r.close(); p.close()
    return render_template("index.html", ranking=ranking, portfolio=portfolio)

if __name__=="__main__":
    app.run(debug=True)
