import streamlit as st
import pandas as pd
from graphviz import Digraph
from huffman_logic import compress
from collections import Counter

st.set_page_config(page_title="Huffman Hub", layout="wide")

st.title("🗜️ Huffman Compression Tool")
st.markdown("Algoritma kompresi lossless untuk segala jenis file.")

with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Pilih file apapun", type=None)

if uploaded_file is not None:
    data = uploaded_file.getvalue()
    with st.spinner("Sedang mengompresi..."):
        compressed, codes, root = compress(data)
    
    orig_size = len(data) * 8
    comp_size = len(compressed)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ukuran Asli", f"{len(data)} bytes")
    col2.metric("Ukuran Kompresi", f"{comp_size/8:.2f} bytes")
    col3.metric("Efisiensi", f"{(1 - (comp_size/orig_size))*100:.1f}%")

    tab1, tab2, tab3 = st.tabs(["📊 Statistik", "🌳 Visualisasi Pohon", "⚙️ Tabel Kode"])
    
    with tab1:
        st.write("Distribusi frekuensi byte:")
        freq_df = pd.DataFrame(Counter(data).items(), columns=['Byte', 'Freq']).sort_values('Freq', ascending=False)
        st.bar_chart(freq_df.set_index('Byte'))
        
    with tab2:
        st.info("Pohon Huffman (Maksimal 100 node pertama untuk performa)")
        dot = Digraph()
        def add_nodes(node, count=0):
            if node and count < 100:
                label = f"{chr(node.char) if node.char and 32<=node.char<=126 else node.char}\n{node.freq}"
                dot.node(str(id(node)), label, shape='circle' if not node.char else 'box')
                if node.left:
                    dot.edge(str(id(node)), str(id(node.left)), '0')
                    add_nodes(node.left, count + 1)
                if node.right:
                    dot.edge(str(id(node)), str(id(node.right)), '1')
                    add_nodes(node.right, count + 1)
        add_nodes(root)
        st.graphviz_chart(dot)

    with tab3:
        st.json(codes)
else:
    st.info("Silakan upload file di sidebar untuk memulai.")
