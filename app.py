import streamlit as st
import os
from workflow import build_workflow

# 1. إعدادات الصفحة والعنوان
st.set_page_config(
    page_title="MADI - MultiAgent Data Intelligence",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 MADI: MultiAgent Data Intelligence Platform")
st.markdown("نظام متكامل من الـ AI Agents للتحليل الآلي للبيانات واسترجاع المعرفة وسرد التقارير الاستراتيجية.")

st.divider()

# 2. شريط الأدوات الجانبي (Sidebar)
st.sidebar.header("⚙️ إعدادات النظام")
uploaded_file = st.sidebar.file_uploader("قم بتحميل ملف البيانات (CSV)", type=["csv"])

task_input = st.sidebar.text_area(
    "المهمة المطلوبة من فريق الـ Agents:",
    value="قم بتحليل أداء البيانات الإحصائية واستخراج الرؤى والتوصيات الرئيسية."
)

start_button = st.sidebar.button("🚀 تشغيل فريق الـ Agents", use_container_width=True)

# 3. المنطقة الرئيسية للمخرجات
if start_button:
    if not uploaded_file:
        st.error("⚠️ يرجى تحميل ملف البيانات (CSV) أولاً لبدء التحليل.")
    else:
        # حفظ الملف المرفوع مؤقتاً
        temp_dir = "./temp_data"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info("🔄 جاري إعداد وتنسيق فريق الـ Agents...")
        
        # إعداد الحالة الأولية (Initial State)
        initial_state = {
            "messages": [],
            "current_task": task_input,
            "data_path": file_path,
            "analysis_result": "",
            "rag_context": "",
            "final_report": ""
        }
        
        # بناء وتشغيل الـ Workflow
        workflow_app = build_workflow()
        
        with st.spinner("🤖 الـ Agents تعمل الآن على معالجة طلبك..."):
            # تنفيذ التدفق
            result_state = workflow_app.invoke(initial_state)
            
        st.success("✅ اكتملت كافة المهام بنجاح!")
        
        # عرض سجل خطوات الـ Agents
        st.subheader("📋 سجل تواصل الـ Agents (Execution Logs)")
        with st.expander("عرض تفاصيل خطوات التفكير والتنسيق"):
            for msg in result_state.get("messages", []):
                st.write(f"- {msg}")
                
        st.divider()
        
        # عرض التقرير النهائي
        st.subheader("📊 التقرير النهائي الصادر من MADI")
        st.markdown(result_state.get("final_report", "لا يوجد تقرير."))
