from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd
import uuid
import os

from .strategy import get_signals_with_stop
from .engine import run_backtest_real, basic_metrics, monte_carlo

app = FastAPI()

# ---------------- HOME PAGE ---------------- #

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Professional Backtest Engine</h2>
    <form action="/run" method="post" enctype="multipart/form-data">
        Upload CSV/XLSX: <input type="file" name="file"><br><br>
        RR: <input type="number" step="0.1" name="rr"><br><br>
        Capital: <input type="number" name="capital"><br><br>
        Risk % per trade: <input type="number" step="0.1" name="risk_percent"><br><br>
        <input type="submit" value="Run Backtest">
    </form>
    """

# ---------------- RUN BACKTEST ---------------- #

@app.post("/run")
async def run(
    file: UploadFile = File(...),
    rr: float = Form(...),
    capital: float = Form(...),
    risk_percent: float = Form(...)
):

    # Load file
    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
    else:
        return {"error": "Upload CSV or XLSX"}

    # Get strategy signals + stop
    signals_df = get_signals_with_stop(df)

    # Run backtest
    R, trades = run_backtest_real(
        df,
        signals_df,
        rr=rr,
        capital=capital,
        risk_percent=risk_percent
    )

    metrics = basic_metrics(R)
    mc = monte_carlo(R)

    # Create logs folder inside container
    os.makedirs("logs", exist_ok=True)

    # Save trade log
    filename = f"trade_logs_{uuid.uuid4().hex}.csv"
    file_path = f"logs/{filename}"

    pd.DataFrame(trades).to_csv(file_path, index=False)

    return {
        "Strategy_Result": metrics,
        "Monte_Carlo": mc,
        "Download_Trade_Log": f"/download/{filename}"
    }

# ---------------- DOWNLOAD ROUTE ---------------- #

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"logs/{filename}"

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=filename
    )
