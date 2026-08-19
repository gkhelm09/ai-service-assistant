# AI BioMed Assistant

A simple Streamlit web application that helps biomedical technician and field service engineers troubleshoot equipment problems. Responses are simulated locally—no external AI API is required.

## Quick Start (easiest)

From the project folder:

```bash
chmod +x run.sh
./run.sh
```

Then open the URL shown in your terminal (usually http://localhost:8501).

## Manual Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS / Linux
   # venv\Scripts\activate    # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open http://localhost:8501 in your browser.

## Troubleshooting

### App will not load / blank page

1. Make sure the virtual environment is activated. Your terminal prompt should show `(venv)`.
2. Reinstall dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Stop any old Streamlit process (`Ctrl+C` in the terminal), then start again with `./run.sh` or `streamlit run app.py`.
4. Check the terminal for red error text. Common fixes:
   - `ModuleNotFoundError: No module named 'streamlit'` → activate `venv` and run `pip install -r requirements.txt`
   - `Address already in use` → another Streamlit instance is still running on port 8501

### Changes to `assistant.py` not appearing

Restart the app (`Ctrl+C`, then run again). The app reloads `assistant.py` on each run.

## Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit user interface |
| `assistant.py` | Simulated response logic (replace with a real AI API later) |
| `requirements.txt` | Python package dependencies |
| `run.sh` | One-command setup and launch script |
| `assets/multimeter.svg` | Custom header icon |
| `README.md` | Setup and usage instructions |

## Next Steps

- Replace the logic in `assistant.py` with calls to an external AI API.
- Add equipment type or model fields for more specific guidance.
- Save troubleshooting history to a database or log file.
