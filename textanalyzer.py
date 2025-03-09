import streamlit as st

st.set_page_config(
    page_title="Text Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    body { background: #f0f2f6; }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Text Analytics")
st.header("Developed by Hasan Raza")

input_text = st.text_area(
    "Enter Your Text",
    height=200,
    placeholder="Enter text here to analyze..."
)

if not input_text.strip():
    st.error("🚨 Please enter valid text to continue!")
    st.stop()

def analyze(text: str) -> dict:
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "vowel_count": sum(1 for c in text.lower() if c in "aeiou"),
        "contains_python": "python" in text.lower(),
        "avg_word_length": round(len(text) / max(len(words), 1), 2)
    }
results = analyze(input_text)

st.subheader("📊 Quick Statistics")
cols = st.columns(4)
cols[0].metric("Total Words", f"{results['word_count']:,}")
cols[1].metric("Total Characters", f"{results['char_count']:,}")
cols[2].metric("Vowel Count", f"{results['vowel_count']:,}")
cols[3].metric("Avg. Word Length", f"{results['avg_word_length']:.2f}")

with st.expander("Advanced Tools", expanded=True):
    tab1, tab2, tab3 = st.tabs(["🔍 Search & Replace", "🔄 Case Conversion", "📌 Insights"])
    with tab1:
        search_term = st.text_input("Search for:")
        replace_term = st.text_input("Replace with:")
        if search_term:
            modified_text = input_text.replace(search_term, replace_term)
            st.code(modified_text, language="text")
    with tab2:
        st.write("### Uppercase Version")
        st.code(input_text.upper(), language="text")
        st.write("### Lowercase Version")
        st.code(input_text.lower(), language="text")
    with tab3:
        special_chars = sum(1 for c in input_text if not c.isalnum() and not c.isspace())
        has_whitespace = "✅ Contains spaces" if ' ' in input_text else "❌ No spaces"
        
        st.subheader("📌 Key Insights")
        st.markdown(f"- **Special Characters:** {special_chars}")
        st.markdown(f"- **Whitespace Analysis:** {has_whitespace}")
st.divider()
st.caption("Built with Streamlit & Python")

