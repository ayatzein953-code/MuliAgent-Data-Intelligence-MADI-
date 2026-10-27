from typing import List, TypedDict, Annotated
import operator

# تعريف الحالة المشتركة التي سيتناقلها الـ Agents
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]  # سجل الرسائل والخطوات
    current_task: str                             # المهمة الحالية المكلّف بها النظام
    data_path: str                                # مسار ملف البيانات (إن وجد)
    analysis_result: str                          # نتيجة التحليل من الـ Data Agent
    rag_context: str                              # المعلومات المسترجعة من الـ RAG Agent
    final_report: str                             # التقرير النهائي المُصدّر
