import heapq
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    freq = Counter(data)
    heap = [Node(char, f) for char, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, current_code, codes):
    if node is None: return
    if node.char is not None:
        codes[node.char] = current_code
    generate_codes(node.left, current_code + "0", codes)
    generate_codes(node.right, current_code + "1", codes)

def compress(data):
    if not data: return "", {}, None
    root = build_huffman_tree(data)
    codes = {}
    generate_codes(root, "", codes)
    compressed_text = "".join([codes[b] for b in data])
    return compressed_text, codes, root
