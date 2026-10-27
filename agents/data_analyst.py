import pandas as pd
import os

def data_analyst_tool(file_path: str) -> str:
    """
    أداة يقوم من خلالها الـ Agent بقراءة ملف البيانات واستخراج تقرير إحصائي أولي.
    """
    if not os.path.exists(file_path):
        return f"عذراً، ملف البيانات غير موجود في المسار: {file_path}"
    
    try:
        # قراءة البيانات (نفترض أن الملف بصيغة CSV)
        df = pd.read_csv(file_path)
        
        # استخراج بعض المعلومات الأساسية
        rows, cols = df.shape
        columns = list(df.columns)
        summary_stats = df.describe().to_string()
        missing_values = df.isnull().sum().to_string()
        
        report = f"""
        [تقرير Data Analyst Agent]
        - حجم البيانات: {rows} صف، {cols} عمود.
        - الأعمدة المتوفرة: {columns}
        
        - إحصائيات وصفية (Summary Statistics):
        {summary_stats}
        
        - القيم المفقودة (Missing Values):
        {missing_values}
        """
        return report
    except Exception as e:
        return f حدث خطأ أثناء تحليل البيانات: {str(e)}"
