# Single-file deploy fix

This build removes the `football_sim` package import completely. It is designed to fix:

```text
ModuleNotFoundError: No module named football_sim
```

Upload every file in this zip directly to the root of the GitHub repo. In Streamlit Cloud, set the main file to:

```text
app.py
```

Then use Manage app -> Reboot app.
