from langgraph.graph import StateGraph, END
from agent_state import AgentState
from agents.data_analyst import data_analyst_tool
from agents.rag_agent import RAGAgent

# 1. تعريف وظائف العُقد (Node Functions) التي تمثل الـ Agents

def data_analyst_node(state: AgentState) -> dict:
    """عقدة وكيل تحليل البيانات"""
    file_path = state.get("data_path", "")
    print("--- [Node] جاري تشغيل Data Analyst Agent ---")
    
    # تشغيل أداة تحليل البيانات
    result = data_analyst_tool(file_path)
    
    # تحديث الحالة المشتركة
    return {
        "analysis_result": result,
        "messages": [f"Data Analyst: تم تحليل ملف البيانات بنجاح."]
    }

def rag_research_node(state: AgentState) -> dict:
    """عقدة وكيل البحث واسترجاع المعرفة"""
    task = state.get("current_task", "")
    print("--- [Node] جاري تشغيل Research & RAG Agent ---")
    
    rag_agent = RAGAgent()
    retrieved_info = rag_agent.search_knowledge_base(task)
    
    return {
        "rag_context": retrieved_info,
        "messages": [f"RAG Agent: تم البحث واسترجاع السياق من قاعدة المعرفة."]
    }

def report_writer_node(state: AgentState) -> dict:
    """عقدة وكيل صياغة التقرير النهائي"""
    print("--- [Node] جاري تشغيل Report Writer Agent ---")
    
    analysis = state.get("analysis_result", "لا يوجد تحليل بيانات.")
    context = state.get("rag_context", "لا يوجد سياق مسترجع.")
    task = state.get("current_task", "")
    
    # هنا يتم تجميع المخرجات من الـ Agents السابقين وصياغة التقرير النهائي
    final_report = f"""
# 📊 التقرير النهائي الشامل: {task}

---

## 🔍 أولاً: نتائج تحليل البيانات الإحصائية
{analysis}

---

## 📚 ثانياً: السياق والمعرفة المسترجعة (RAG Context)
{context}

---

## 💡 ثالثاً: التوصيات والرؤى الاستراتيجية
- بناءً على الأرقام والسياق اعلاه، يُوصى بالتركيز على تحسين كفاءة البيانات واستغلال الفرص المتاحة.
- هذا التقرير تم إنشاؤه آلياً بواسطة نظام الـ Multi-Agent الذكي.
"""
    return {
        "final_report": final_report,
        "messages": [f"Report Writer: تم إنشاء التقرير النهائي بنجاح."]
    }

# 2. بناء الهيكل والروابط (LangGraph Construction)

def build_workflow():
    workflow = StateGraph(AgentState)
    
    # إضافة العُقد (Nodes)
    workflow.add_node("data_analyst", data_analyst_node)
    workflow.add_node("rag_researcher", rag_research_node)
    workflow.add_node("report_writer", report_writer_node)
    
    # تحديد نقطة البداية (Entry Point)
    workflow.set_entry_point("data_analyst")
    
    # تحديد الحواف والمسار (Edges)
    workflow.add_edge("data_analyst", "rag_researcher")
    workflow.add_edge("rag_researcher", "report_writer")
    workflow.add_edge("report_writer", END)
    
    # تجميع الرسم البياني (Compile Graph)
    app = workflow.compile()
    return app
