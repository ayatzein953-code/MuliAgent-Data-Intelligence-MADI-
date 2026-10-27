from langchain_community.llms import Ollama

class ReportWriterAgent:
    def init(self, model_name: str = "llama3.2"):
        """
        تهيئة وكيل صياغة التقارير باستخدام نموذج Ollama محلي
        """
        try:
            self.llm = Ollama(model=model_name)
        except Exception as e:
            self.llm = None
            print(f"تنبيه: لم يتم الاتصال بـ Ollama بشكل مباشر: {e}")

    def generate_report(self, task: str, analysis_result: str, rag_context: str) -> str:
        """
        تجميع نتائج الـ Agents وصياغة تقرير احترافي بتنسيق Markdown
        """
        prompt = f"""
أنت وكيل خبير في صياغة التقارير الاستراتيجية وتحليل الأعمال (Report Writer Agent).
بناءً على البيانات والتحليلات التالية، قم بكتابة تقرير شامل، منسق، واحترافي باللغة العربية بتنسيق Markdown.

المهمة المطلوبة: {task}

1. نتائج تحليل البيانات (Data Analyst Result):
{analysis_result}

2. السياق والمعرفة المسترجعة (RAG Context):
{rag_context}

تعليمات الصياغة:
- استخدم عناوين واضحة (Headings) ونقاط محددة.
- ابدأ بملخص تنفيذي (Executive Summary).
- عرض أهم الأرقام والمؤشرات الإحصائية.
- استخراج التوصيات والرؤى الاستراتيجية للعمل.
"""

        # إذا كان نموذج Ollama يعمل محلياً، نستخدمه للصياغة الذكية
        if self.llm:
            try:
                response = self.llm.invoke(prompt)
                return response
            except Exception:
                pass

        # في حال عدم توفر Ollama محلياً في لحظة التشغيل، نستخدم القالب الاحترافي الجاهز:
        return f"""
# 📊 التقرير الاستراتيجي الشامل - MADI Platform

---

## 📝 الملخص التنفيذي
تم إعداد هذا التقرير آلياً بواسطة نظام MADI لنقل وتجميع نتائج تحليل البيانات والسياق المسترجع للطلب: "{task}".

---

## 🔍 أولاً: نتائج تحليل البيانات الإحصائية
{analysis_result}

---

## 📚 ثانياً: السياق والمعرفة المسترجعة (RAG Context)
{rag_context}

---

## 💡 ثالثاً: التوصيات والرؤى الاستراتيجية
* تحسين كفاءة البيانات: الاعتماد على المؤشرات الإحصائية المستخرجة لتوجيه القرارات الإدارية.
* دعم القرار بالذكاء الاصطناعي: دمج نتائج الـ RAG مع البيانات الرقمية يضمن فهم السياق الكامل للسوق.
* الخطوة القادمة: متابعة الأداء بصفة دورية وتحديث قاعدة المعرفة الخاصة بالنظام.
"""
