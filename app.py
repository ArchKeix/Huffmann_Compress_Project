import streamlit as st
import pandas as pd
from graphviz import Digraph
from huffman_logic import compress

st.set_page_config(page_title="Huffman Visualizer", layout="wide")
st.title("🗜️ Huffman Compression Visualizer")

uploaded_file = st.file_uploader("Drag & Drop file teks Anda", type=['txt'])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    
    # 1. Kompresi
    compressed, codes, root = compress(text)
    
    # 2. Statistik
    orig_size = len(text) * 8 # bit
    comp_size = len(compressed) # bit
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Statistik")
        st.write(f"Ukuran Awal: {orig_size} bits")
        st.write(f"Ukuran Kompresi: {comp_size} bits")
        if orig_size > 0:
            st.write(f"Rasio Kompresi: {100 - (comp_size/orig_size*100):.2f}% lebih hemat")
    
    with col2:
        st.subheader("Distribusi Frekuensi")
        freq_df = pd.DataFrame(list(dict(pd.Series(list(text)).value_counts()).items()), columns=['Char', 'Freq'])
        st.dataframe(freq_df)

    # 3. Visualisasi Pohon
    st.subheader("Visualisasi Pohon Huffman")
    dot = Digraph()
    
    def add_nodes(node):
        if node:
            label = f"{node.char if node.char else ' '}\n{node.freq}"
            dot.node(str(id(node)), label)
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)), '0')
                add_nodes(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)), '1')
                add_nodes(node.right)
    
    add_nodes(root)
    st.graphviz_chart(dot)
