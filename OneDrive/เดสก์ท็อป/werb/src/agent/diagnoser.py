def diagnose(new_cols, missing_cols):
    if new_cols and not missing_cols:
        return {"class":"schema_drift","confidence":0.9,"note":"New columns detected"}
    if missing_cols and not new_cols:
        return {"class":"missing_columns","confidence":0.95,"note":"Required columns missing"}
    if new_cols and missing_cols:
        return {"class":"mixed_schema_change","confidence":0.7,"note":"Both new and missing columns"}
    return {"class":"ok","confidence":1.0,"note":"No drift detected"}
