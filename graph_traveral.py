import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Graph Object
G = nx.Graph()
pos = {}

# Main Window
root = tk.Tk()
root.title("Graph Traversal Visualization")
root.geometry("900x700")

# Frame Layout
top_frame = tk.Frame(root)
top_frame.pack()

graph_frame = tk.Frame(root)
graph_frame.pack()

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(5,5))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

# -------- Graph Drawing --------
def draw_graph():
    ax.clear()
    nx.draw(G, pos, ax=ax, with_labels=True,
            node_size=2000,
            font_size=10)
    canvas.draw()

# -------- Add Edge --------
def add_edge():
    global pos

    u = node1_entry.get()
    v = node2_entry.get()

    if u and v:
        G.add_edge(u, v)

        # Update Layout
        pos = nx.spring_layout(G)

        draw_graph()
    else:
        messagebox.showerror("Error", "Enter valid nodes")

# -------- BFS Animation --------
def bfs_animation():
    start = start_entry.get()

    if start not in G.nodes:
        messagebox.showerror("Error", "Start node not found")
        return

    visited = set()
    queue = deque([start])
    visited.add(start)

    traversal = []

    while queue:
        node = queue.popleft()
        traversal.append(node)

        for neighbor in G[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    animate_traversal(traversal, "BFS Traversal")

# -------- DFS Animation --------
def dfs_animation():
    start = start_entry.get()

    if start not in G.nodes:
        messagebox.showerror("Error", "Start node not found")
        return

    traversal = []

    def dfs(node, visited=set()):
        visited.add(node)
        traversal.append(node)

        for neighbor in G[node]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    dfs(start)
    animate_traversal(traversal, "DFS Traversal")

# -------- Animation Function --------
def animate_traversal(traversal, title):

    for node in traversal:
        ax.clear()

        node_colors = []
        for n in G.nodes():
            node_colors.append("red" if n == node else "skyblue")

        nx.draw(G, pos, ax=ax,
                with_labels=True,
                node_color=node_colors,
                node_size=2000)

        ax.set_title(title)
        canvas.draw()

        root.update()
        root.after(800)

# -------- Shortest Path --------
def shortest_path():
    src = src_entry.get()
    dst = dst_entry.get()

    try:
        path = nx.shortest_path(G, source=src, target=dst)

        ax.clear()
        nx.draw(G, pos, ax=ax,
                with_labels=True,
                node_size=2000)

        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos,
                               edgelist=edges,
                               width=3,
                               ax=ax)

        canvas.draw()

    except:
        messagebox.showerror("Error", "Path not found")

# -------- UI Components --------
tk.Label(top_frame, text="Node1").grid(row=0, column=0)
node1_entry = tk.Entry(top_frame)
node1_entry.grid(row=0, column=1)

tk.Label(top_frame, text="Node2").grid(row=0, column=2)
node2_entry = tk.Entry(top_frame)
node2_entry.grid(row=0, column=3)

tk.Button(top_frame, text="Add Edge", command=add_edge).grid(row=0, column=4)

# Traversal Inputs
tk.Label(top_frame, text="Start Node").grid(row=1, column=0)
start_entry = tk.Entry(top_frame)
start_entry.grid(row=1, column=1)

tk.Button(top_frame, text="BFS", command=bfs_animation).grid(row=1, column=2)
tk.Button(top_frame, text="DFS", command=dfs_animation).grid(row=1, column=3)

# Shortest Path
tk.Label(top_frame, text="Source").grid(row=2, column=0)
src_entry = tk.Entry(top_frame)
src_entry.grid(row=2, column=1)

tk.Label(top_frame, text="Destination").grid(row=2, column=2)
dst_entry = tk.Entry(top_frame)
dst_entry.grid(row=2, column=3)

tk.Button(top_frame, text="Shortest Path", command=shortest_path).grid(row=2, column=4)

# Draw Initial Graph Button
tk.Button(root, text="Show Graph", command=draw_graph,
          font=("Arial", 12)).pack(pady=10)

root.mainloop()