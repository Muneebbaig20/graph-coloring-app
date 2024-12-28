

import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time #for noting execution time
#for memory usage
import psutil
import os


class GraphVisualizer:
    def __init__(self, root):
        self.root_window = root
        self.root_window.title("Graph Visualization Tool")
        self.graph_data = nx.Graph()
        self.node_positions = {}  
        self.nodes_added = False
        self.edges_added = False
        self.figure = plt.figure(figsize=(6, 4))  
        self.canvas = None
        self.create_widgets()

    def create_widgets(self):
        # Instructions
        self.instructions_label = tk.Label(
            self.root_window,
            text="1. Add Vertices\n2. Add Edges\n3. Choose Coloring",
            font=("Arial", 12),
        )
        self.instructions_label.pack()

        # Buttons
        self.add_nodes_button = tk.Button(
            self.root_window, text="Add Vertices", command=self.add_nodes
        )
        self.add_nodes_button.pack(pady=5)

        self.add_edges_button = tk.Button(
            self.root_window, text="Add Edges", command=self.add_edges, state=tk.DISABLED
        )
        self.add_edges_button.pack(pady=5)

        self.choose_coloring_button = tk.Button(
            self.root_window, text="Choose Coloring", command=self.choose_coloring, state=tk.DISABLED
        )
        self.choose_coloring_button.pack(pady=5)

        self.quit_button = tk.Button(self.root_window, text="Quit", command=self.root_window.quit)
        self.quit_button.pack(pady=5)

    def add_nodes(self):
        if self.nodes_added:
            messagebox.showinfo("Info", "Vertices already added!")
            return

        num_nodes = simpledialog.askinteger("Vertices", "Enter number of vertices:")
        if num_nodes:

            nodes = [chr(65 + i) for i in range(num_nodes)]
            self.graph_data.add_nodes_from(nodes)

            # Assign fixed positions in a circular layout
            self.node_positions = nx.circular_layout(self.graph_data)
            self.nodes_added = True
            
            self.plot_graph()
            messagebox.showinfo("Vertex Added", f"Added {num_nodes} vertices!")
            self.add_edges_button.config(state=tk.NORMAL)
            

    
    def add_edges(self):
        if not self.nodes_added:
            messagebox.showerror("Error", "Add vertices first!")
            return

        while True:
            edge = simpledialog.askstring(
                "Edges", "Enter an edge (e.g., A-B). Leave blank or cancel to finish:"
            )
            if not edge:
                break
            try:
                v1, v2 = edge.split("-")
                if (v1, v2) in self.graph_data.edges or (v2, v1) in self.graph_data.edges:
                    messagebox.showwarning("Duplicate Edge", "Edge already added!")
                elif v1 in self.graph_data.nodes and v2 in self.graph_data.nodes:
                    self.graph_data.add_edge(v1, v2)
                    self.plot_graph()
                else:
                    messagebox.showerror(
                        "Invalid Edge", f"Nodes {v1} and/or {v2} do not exist."
                    )

        
            except ValueError:
                messagebox.showerror(
                    "Invalid Input", "Please enter edges in the format A-B."
                )

        self.edges_added = True
        self.choose_coloring_button.config(state=tk.NORMAL)

    def choose_coloring(self):
        if not self.edges_added:
            messagebox.showerror("Error", "Add edges first!")
            return

        choice = simpledialog.askstring(
            "Coloring",
            "Type 'vertex' for vertex coloring or 'edge' for edge coloring:",
        )
        if choice == "vertex":
            self.color_nodes()
        elif choice == "edge":
            self.color_edges()
        else:
            messagebox.showerror("Invalid Choice", "Please choose 'node' or 'edge'.")

    def add_heading(self, text):
        if hasattr(self, "heading_label") and self.heading_label.winfo_exists():
            self.heading_label.config(text=text)
        else:
            self.heading_label = tk.Label(self.root_window, text=text, font=("Arial", 14, "bold"))

        self.heading_label.pack(side="top", before=self.canvas.get_tk_widget() if self.canvas else None)

    def color_nodes(self):
        start_time = time.time()  # Start timing
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024  # Initial memory usage

        colors = nx.coloring.greedy_color(self.graph_data, strategy="largest_first")
        node_colors = [colors[node] for node in self.graph_data.nodes]
        self.plot_graph(node_colors=node_colors)
        chromatic_number = len(set(colors.values()))
        heading = f"Chromatic Number: {chromatic_number}"
        self.add_heading(heading)

        end_time = time.time()  # End timing
        final_memory = process.memory_info().rss / 1024  # Final memory usage
        
        messagebox.showinfo("vertex Coloring", "vertex coloring applied!")
        
        print(f"\n\nTime for vertex coloring: {(end_time - start_time) * 1000} milliseconds\n")
        print(f"Memory Usage for vertex coloring: {final_memory - initial_memory} KB")
    
    def color_edges(self):
        start_time = time.time()  # Start timing
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024  # Initial memory usage

    
        colors = nx.coloring.greedy_color(nx.line_graph(self.graph_data), strategy="largest_first")
        edge_colors = [colors[edge] for edge in self.graph_data.edges]
        self.plot_graph(edge_colors=edge_colors)
        chromatic_index = len(set(colors.values()))
        heading = f"Chromatic Index: {chromatic_index}"
        self.add_heading(heading)
 
        end_time = time.time()  # End timing
        final_memory = process.memory_info().rss / 1024  # Final memory usage
        
        messagebox.showinfo("Edge Coloring", "Edge coloring applied!")

        print(f"\n\nTime for edge coloring: {(end_time - start_time) * 1000} milliseconds\n")
        print(f"Memory Usage for edge coloring: {final_memory - initial_memory} KB")
    
    
    def plot_graph(self, node_colors=None, edge_colors=None):
        self.figure.clf()

        ax = self.figure.add_subplot(1, 1, 1)
        nx.draw(
            self.graph_data,
            pos=self.node_positions,
            with_labels=True,
            node_color=node_colors if node_colors else "lightblue",
            edge_color=edge_colors if edge_colors else "black",
            node_size=500,
            font_size=10,
            ax=ax,
        )

        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

# Main application
if __name__ == "__main__":
    root_window = tk.Tk()
    graph_visualizer = GraphVisualizer(root_window)
    root_window.mainloop()
