import streamlit as st
import pandas as pd
import plotly.express as px
from model import train_and_evaluate, predict_topic
from content import PATHS, QUIZ, SCENARIOS

st.set_page_config(page_title="Cyber Mentor | المرشد السيبراني", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap');
:root{--bg:#07141c;--panel:#0d222c;--line:#1c4850;--mint:#62d6ad;--muted:#9ab4b8}
html,body,[class*="css"]{direction:rtl;text-align:right;font-family:'IBM Plex Sans Arabic',sans-serif}
.stApp{background:radial-gradient(circle at 85% 0%,#123b3b 0%,#07151d 42%,#061018 100%);color:#e8f1f2}
section[data-testid="stSidebar"]{background:#081820;border-left:1px solid var(--line)}
.block-container{max-width:1320px;padding-top:1.5rem}
h1,h2,h3{color:#effafa!important}
p,label,.stMarkdown{color:#c5d6d8}
div[data-testid="stMetric"]{background:linear-gradient(145deg,#102b32,#0b2029);border:1px solid var(--line);padding:14px;border-radius:14px}
div[data-testid="stMetricValue"]{color:var(--mint)}
.stButton>button,.stFormSubmitButton>button{background:#087e69;color:white;border:1px solid #2ba98b;border-radius:10px;font-weight:700;min-height:2.7rem}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#21a987;color:#061018}
.panel{background:rgba(13,38,47,.9);border:1px solid var(--line);border-radius:16px;padding:20px;margin:10px 0 16px}
.kicker{color:var(--mint);font-size:.8rem;font-weight:700;letter-spacing:1px}
.hero{font-size:2rem;font-weight:700;color:#f1ffff;margin:5px 0}
.muted{color:var(--muted);line-height:1.9}
.tag{display:inline-block;border:1px solid #2b7167;color:#8be7bf;background:#0d302d;border-radius:30px;padding:4px 11px;margin:3px;font-size:.8rem}
div[data-testid="stProgressBar"]>div>div{background:#4bd2a0}
[data-testid="stExpander"]{border:1px solid var(--line);border-radius:12px}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_model():
    return train_and_evaluate()

model, metrics = get_model()

PAGES = ["الرئيسية", "اختبار المهارات", "نتيجتي وخطتي", "مركز التعلم", "تحديات المواقف", "منهجية النموذج"]
with st.sidebar:
    st.markdown("## 🛡️ CYBER MENTOR")
    st.caption("المرشد السيبراني | LEARNING & AWARENESS")
    st.markdown('<span class="tag">SOC INSPIRED</span><span class="tag">AI LEARNING</span>', unsafe_allow_html=True)
    page = st.radio("التنقل", PAGES, label_visibility="collapsed")
    st.divider()
    st.caption("نسخة تعليمية تجريبية · 2026")
    st.caption("لا تجمع المنصة بيانات شخصية ولا تفحص الأجهزة أو الشبكات.")

def hero(kicker, title, subtitle):
    st.markdown(f'<div class="panel"><div class="kicker">{kicker}</div><div class="hero">{title}</div><div class="muted">{subtitle}</div></div>', unsafe_allow_html=True)

def go(page_name):
    st.session_state["page_jump"] = page_name

if "page_jump" in st.session_state:
    page = st.session_state.pop("page_jump")

if page == "الرئيسية":
    hero("SECURITY OPERATIONS / LEARNING HUB", "مرحبًا بك في Cyber Mentor",
         "منصة تدريبية تحوّل تقييم المعرفة السيبرانية إلى خطة تعلم عملية. اختبر فهمك، اكتشف المجال الذي يحتاج إلى تعزيز، ثم طبّق ما تعلمته في مواقف تفاعلية.")
    c1,c2,c3 = st.columns(3)
    c1.metric("أسئلة التقييم", "15", "5 لكل مجال")
    c2.metric("مسارات التعلم", "03", "محتوى موجّه")
    c3.metric("تحديات تطبيقية", str(len(SCENARIOS)), "مواقف قصيرة")
    st.markdown("### مركز العمليات التعليمية")
    cols = st.columns(3)
    for col, (key, path) in zip(cols, PATHS.items()):
        with col:
            st.markdown(f'<div class="panel"><div class="kicker">{path["code"]} / LEARNING PATH</div><h3>{path["title"]}</h3><p class="muted">{path["summary"]}</p></div>', unsafe_allow_html=True)
    st.markdown("### رحلة المتعلم")
    st.markdown('<div class="panel"><span class="tag">01 · قيّم</span><span class="tag">02 · حلّل</span><span class="tag">03 · تعلّم</span><span class="tag">04 · طبّق</span><p class="muted">يجيب المتعلم عن 15 سؤالًا، وتُحوّل الإجابات إلى درجات للمجالات الثلاثة. تستخدم شجرة القرار الدرجات لتحديد أولوية التعلم، ثم تعرض المنصة توصيات ومحتوى وتحديات مرتبطة بالنتيجة.</p></div>', unsafe_allow_html=True)
    st.info("ابدأ من «اختبار المهارات». لا تدخل اسمك أو بريدك أو أي معلومات شخصية.")

elif page == "اختبار المهارات":
    hero("LEARNER ASSESSMENT / 01", "اختبار الوعي السيبراني",
         "15 سؤال اختيار من متعدد. اختر الإجابة الأنسب لكل موقف. تُستخدم الإجابات لحساب مستوى كل مجال وتحديد أولوية التعلم.")
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    with st.form("quiz_form"):
        for i, q in enumerate(QUIZ):
            st.markdown(f"**{i+1:02d}. {q['question']}**")
            choice = st.radio("اختر إجابة:", q["options"], key=f"q_{i}", index=None, label_visibility="collapsed")
            st.session_state.quiz_answers[str(i)] = choice
            st.markdown("---")
        submitted = st.form_submit_button("تحليل إجاباتي", use_container_width=True)
    if submitted:
        missing = [str(i) for i in range(len(QUIZ)) if not st.session_state.quiz_answers.get(str(i))]
        if missing:
            st.warning(f"أكمل جميع الأسئلة أولًا. الأسئلة المتبقية: {len(missing)}")
        else:
            scores = {k: {"correct":0,"total":0} for k in PATHS}
            for i,q in enumerate(QUIZ):
                k=q["domain"]; scores[k]["total"] += 1
                if st.session_state.quiz_answers[str(i)] == q["answer"]:
                    scores[k]["correct"] += 1
            percentages = {k: round(v["correct"]/v["total"]*100) for k,v in scores.items()}
            errors = sum(v["total"]-v["correct"] for v in scores.values())
            pred, confidence = predict_topic(model, percentages, errors)
            st.session_state.result = {"scores":percentages,"raw":scores,"errors":errors,"prediction":pred,"confidence":confidence}
            st.success("اكتمل التحليل. افتح صفحة «نتيجتي وخطتي» لعرض التقرير.")
            st.button("عرض خطتي التعليمية", on_click=go, args=("نتيجتي وخطتي",))

elif page == "نتيجتي وخطتي":
    hero("PERSONAL LEARNING PLAN / 02", "نتيجتك وخطتك التعليمية",
         "تقرير محلي داخل الجلسة الحالية. لا يتم حفظ إجاباتك في قاعدة بيانات.")
    result = st.session_state.get("result")
    if not result:
        st.warning("لم تُجرِ الاختبار بعد. انتقل إلى صفحة اختبار المهارات أولًا.")
        if st.button("الانتقال إلى الاختبار"): go("اختبار المهارات")
    else:
        scores=result["scores"]
        st.markdown("### مؤشرات المجالات")
        cols=st.columns(3)
        for col,(key,path) in zip(cols,PATHS.items()):
            with col: col.metric(path["title"],f'{scores[key]}%',f'{result["raw"][key]["correct"]} من 5 إجابات صحيحة')
        st.markdown("### تحليل شجرة القرار")
        st.markdown(f'<div class="panel"><div class="kicker">MODEL OUTPUT</div><h2>{PATHS[result["prediction"]]["title"]}</h2><p class="muted">هذا المجال هو أولوية التدريب المقترحة بناءً على درجات المجالات الثلاثة وعدد الإجابات غير الصحيحة.</p><span class="tag">ثقة النموذج: {result["confidence"]*100:.1f}%</span></div>', unsafe_allow_html=True)
        st.caption("درجة الثقة هي احتمال النموذج للفئة المختارة ضمن الفئات التي تعلمها؛ لا تعني احتمالًا طبيًا أو حكمًا قطعيًا على المتعلم.")
        st.markdown("### توصياتك")
        rec=PATHS[result["prediction"]]
        for item in rec["recommendations"]: st.markdown(f"- {item}")
        st.markdown("### الخطوة التالية")
        st.write(rec["next_step"])
        if st.button("افتح مسار التعلم المقترح", use_container_width=True): go("مركز التعلم")

elif page == "مركز التعلم":
    hero("KNOWLEDGE BASE / 03", "مركز التعلم", "ثلاثة مسارات قصيرة: مفهوم أساسي، مؤشرات يجب الانتباه لها، وممارسات وقائية قابلة للتطبيق.")
    tabs=st.tabs([p["title"] for p in PATHS.values()])
    for tab,(key,path) in zip(tabs,PATHS.items()):
        with tab:
            st.markdown(f"### {path['title']}")
            st.write(path["summary"])
            for section in path["sections"]:
                with st.expander(section["heading"], expanded=True):
                    st.write(section["body"])
                    for bullet in section.get("bullets",[]): st.markdown(f"- {bullet}")
            st.success(f"تطبيق عملي: {path['practice']}")

elif page == "تحديات المواقف":
    hero("SCENARIO TRAINING / 04", "تحديات المواقف التفاعلية", "اتخذ قرارًا في مواقف رقمية شائعة، ثم اقرأ تفسير الإجابة. الهدف هو التعلم من القرار وليس جمع النقاط فقط.")
    for i,sc in enumerate(SCENARIOS):
        with st.expander(f"التحدي {i+1:02d} · {sc['title']}", expanded=(i==0)):
            st.write(sc["situation"])
            choice=st.radio("ما التصرف الأنسب؟",sc["options"],key=f"scenario_{i}",index=None)
            if st.button("تحقق من قراري",key=f"check_{i}"):
                if choice is None: st.warning("اختر إجابة أولًا.")
                elif choice == sc["answer"]:
                    st.success("قرار مناسب. "+sc["explanation"])
                else:
                    st.error("هذا ليس الخيار الأكثر أمانًا. "+sc["explanation"])
                st.info("قاعدة تذكّرها: "+sc["rule"])

elif page == "منهجية النموذج":
    hero("MODEL CARD / 05", "منهجية النموذج ومقاييس التقييم", "تشرح هذه الصفحة مصدر البيانات، طريقة التدريب، حدود الاستخدام، وكيفية قراءة مصفوفة الالتباس.")
    st.markdown("### بنية شجرة القرار")
    st.write("تُستخدم ثلاثة متغيرات إدخال: درجة التصيد الإلكتروني، ودرجة الخصوصية، ودرجة كلمات المرور (كل منها من 0 إلى 100)، إضافة إلى عدد الإجابات غير الصحيحة. يتنبأ النموذج بأولوية المسار التعليمي.")
    st.code("المدخلات → DecisionTreeClassifier → المسار ذو أولوية التدريب", language="text")
    a,b,c=st.columns(3)
    a.metric("Accuracy",f'{metrics["accuracy"]*100:.1f}%')
    b.metric("Precision (weighted)",f'{metrics["precision"]*100:.1f}%')
    c.metric("Recall (weighted)",f'{metrics["recall"]*100:.1f}%')
    st.caption(f'حجم البيانات: {metrics["total_size"]} سجلًا اصطناعيًا · تدريب: {metrics["train_size"]} · اختبار: {metrics["test_size"]}.')
    labels=metrics["labels"]
    cm=pd.DataFrame(metrics["confusion_matrix"],index=labels,columns=labels)
    st.markdown("### مصفوفة الالتباس")
    st.caption("الصفوف = الفئة الحقيقية في البيانات الاصطناعية، والأعمدة = الفئة التي تنبأ بها النموذج.")
    st.dataframe(cm,use_container_width=True)
    fig=px.imshow(cm,text_auto=True,aspect="auto",labels=dict(x="الفئة المتوقعة",y="الفئة الفعلية",color="عدد السجلات"),color_continuous_scale="Teal")
    st.plotly_chart(fig,use_container_width=True)
    st.markdown("### كيف صُنعت البيانات؟")
    st.write("الملف المرفق يحتوي بيانات اصطناعية مولدة برمجيًا لأغراض اختبار خط التدريب والتقييم. وُضعت الفئة المرجعية وفق المجال الأقل درجة، مع قاعدة كسر تعادل ثابتة. لذلك يتعلم النموذج تقريب قاعدة التوليد؛ لا تمثل هذه البيانات عينة بشرية ولا تثبت فاعلية تربوية.")
    st.markdown("### تعريف المقاييس")
    st.markdown("- **Accuracy:** نسبة التنبؤات الصحيحة من إجمالي سجلات الاختبار.\n- **Precision:** من السجلات التي تنبأ النموذج بانتمائها إلى فئة، ما نسبة الصحيح منها؛ مع متوسط موزون حسب دعم الفئات.\n- **Recall:** نسبة سجلات كل فئة التي استعادها النموذج بصورة صحيحة؛ مع متوسط موزون.\n- **مصفوفة الالتباس:** تفصل الصحيح والخطأ لكل فئة.")
    st.warning("لا تستخدم المخرجات لاتخاذ قرارات أمنية فعلية أو لتصنيف قدرات الأشخاص. قبل أي ادعاء بحثي، يلزم تحكيم الأسئلة، وجمع بيانات مناسبة بموافقة الجهات المعنية، وفصل بيانات التدريب عن الاختبار، وإجراء تحقق مستقل.")
    st.markdown("### حدود النموذج")
    st.markdown("- التوصية تعليمية وليست تشخيصًا أو شهادة كفاءة.\n- ثقة النموذج ليست مقياسًا موثوقًا لمستوى الشخص.\n- البيانات الحالية اصطناعية، والنتائج المعروضة تصف أداءً على تقسيم اصطناعي فقط.\n- لا يتصل التطبيق بأجهزة أو شبكات، ولا يجمع كلمات مرور أو بيانات تعريفية.")
