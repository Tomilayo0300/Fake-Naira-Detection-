# 💵 Fake Naira Detection

A Streamlit web app that detects fake vs genuine Nigerian Naira notes using a MobileNetV2 model.  
Deployed directly to **Azure Web App** from GitHub — no CI/CD workflow file needed.

## Project structure

```
├── src/
│   └── app.py                   # Streamlit web app
├── models/
│   └── naira_fake_vs_genuine_model.h5
├── notebooks/
│   ├── chapter_3_rbs.py         # Training script (Colab origin)
│   └── Chapter_3_RBS.ipynb      # Research notebook
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Quick start (local)

```powershell
uv sync
uv run streamlit run src/app.py
```

## Deploy to Azure Web App

1. **Create a Web App** in Azure Portal → Linux, Python 3.12 runtime.
2. **Deployment Center** → Source: **GitHub** → select your repo and the `uv-app` branch.  
   Azure will auto-detect `pyproject.toml` and install dependencies on every push.
3. **Configuration → General settings → Startup Command**:
   ```
   python -m streamlit run src/app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true
   ```

That's it — no secrets, no workflow files required.

## Useful uv commands

```powershell
uv lock        # Refresh lock file after dependency changes
uv sync        # Recreate .venv from lock
```
