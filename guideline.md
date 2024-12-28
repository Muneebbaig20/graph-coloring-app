# Graph Visualization Tool

This project is a Python-based graphical user interface (GUI) tool for visualizing and manipulating graphs. It allows users to:
1. Add vertices (nodes) to the graph.
2. Add edges between the vertices.
3. Apply vertex and edge coloring using a greedy coloring algorithm.
4. Display the graph with the applied colors in a Tkinter window.

The tool uses **NetworkX** for graph manipulation and **Matplotlib** for plotting the graphs.

## Features

- **Add Vertices**: Allows users to add nodes to the graph.
- **Add Edges**: Connects the vertices with edges.
- **Vertex Coloring**: Uses the greedy coloring algorithm to color the nodes of the graph.
- **Edge Coloring**: Uses the greedy coloring algorithm on the line graph of the graph to color the edges.
- **Graph Display**: Displays the graph with labels, colors, and layout.

## Prerequisites

To run this project, you need to install the following Python libraries:

1. **NetworkX** for graph creation and manipulation.
2. **Matplotlib** for graph plotting.

You can install these dependencies using `pip`:

```bash
pip install networkx
pip install matplotlib
