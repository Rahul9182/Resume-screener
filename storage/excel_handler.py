import pandas as pd
from pathlib import Path

def save_to_excel(df, out_path=None, selected_columns=None, merge=True):
    if out_path is None:
        out_path = Path('output') / 'resume_data.xlsx'
    Path('output').mkdir(exist_ok=True)

    # Restrict columns if requested
    if selected_columns:
        existing_cols = [c for c in selected_columns if c in df.columns]
        df_to_save = df[existing_cols].copy()
    else:
        df_to_save = df.copy()

    if merge:
        # Load existing if present to merge (deduplicated)
        if Path(out_path).exists():
            try:
                existing = pd.read_excel(out_path)
            except Exception:
                existing = pd.DataFrame()
        else:
            existing = pd.DataFrame()

        # Union columns
        all_cols = list(dict.fromkeys(list(existing.columns) + list(df_to_save.columns)))
        existing = existing.reindex(columns=all_cols)
        df_to_save = df_to_save.reindex(columns=all_cols)

        # Merge and de-duplicate rows by stable identifiers
        combined = pd.concat([existing, df_to_save], ignore_index=True)

        # Prefer unique resume_id if available
        if 'resume_id' in combined.columns:
            combined = combined.drop_duplicates(subset=['resume_id'], keep='last')
        # Otherwise, try a best-effort on file_name + upload_date
        elif all(c in combined.columns for c in ['file_name', 'upload_date']):
            combined = combined.drop_duplicates(subset=['file_name', 'upload_date'], keep='last')

        # Normalize missing values for consistent Excel output
        combined = combined.fillna('Not Found')

        combined.to_excel(out_path, index=False)
    else:
        # Overwrite mode: write exactly the provided dataframe
        df_to_save = df_to_save.fillna('Not Found')
        df_to_save.to_excel(out_path, index=False)
    return str(out_path)

def load_from_excel(path=None):
    if path is None:
        path = Path('output') / 'resume_data.xlsx'
    if Path(path).exists():
        return pd.read_excel(path)
    return None