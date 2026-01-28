from mcp.server.fastmcp import FastMCP
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# สร้าง Instance ของ FastMCP
mcp = FastMCP("PyCaret-MCP-Server")

@mcp.tool()
def analyze_csv_data(file_path: str, target_column: str):
    """เครื่องมือสำหรับวิเคราะห์ไฟล์ CSV และรายงานผล Accuracy เบื้องต้น"""
    try:
        df = pd.read_csv(file_path)
        # จำลองการทำงานของ ML Pipeline
        X = df.select_dtypes(include=[np.number])
        if target_column in X.columns:
            X = X.drop(columns=[target_column])
        y = df[target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=50)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        
        return f"วิเคราะห์เสร็จสิ้น: โมเดล Random Forest ให้ค่า Accuracy ประมาณ {score:.4f}"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"

@mcp.resource("model://summary")
def get_model_summary():
    """แสดงข้อมูลสรุปของโมเดลที่ใช้งานล่าสุด"""
    return "Model: Random Forest | Status: Trained | Ready for Critique"

if __name__ == "__main__":
    mcp.run()