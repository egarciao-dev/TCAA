# Student Name: Eduardo Garcia Ortiz
# Titan Email: eduardoga@csu.fullerton.edu
# Project: CPSC 335 – Titan Campus Algorithmic Assistant (TCAA)
# Date: 12/06/2025

import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import os
import PyPDF2
from docx import Document
from PIL import Image, ImageTk
from pathlib import Path

from .campus_algorithms import *
from .note_search_algorithms import (naive_string_match, rabin_karp, kmp_search)

    
class TCAAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Titan Campus Algorithmic Assistant (TCAA)")
        self.geometry("1100x700")
        self.minsize(1200, 930)

        style = ttk.Style(self)
        style.theme_use("clam")

        self.zoom_factor = 1.0
        self.min_zoom = 0.4
        self.max_zoom = 3.0
        self.base_scale = 1.0
        
        self.notes_files = []  # list of dicts: {"name": str, "path": str, "text": str}
        self.loaded_text = ""

        #  BUILDING NODE COORDINATES
        self.building_positions = {
            "AD":   (302, 575),
            "AF":   (278, 191),
            "ASC":  (29, 444),
            "B":    (194, 416),
            "CC":   (117, 206),
            "CJ":   (326, 554),
            "CP":   (330, 646),
            "CPAC": (197, 489),
            "CS":   (374, 397),
            "CY":   (88, 283),
            "DBH":  (226, 564),
            "E":    (352, 396),
            "EC":   (305, 446),
            "ENPS": (423, 467),
            "ESPS": (418, 505),
            "GAH":  (83, 393),
            "GAS":  (400, 351),
            "GC":   (185, 538),
            "GF":   (256, 141),
            "GH":   (310, 535),
            "H":    (311, 492),  
            "HRE":  (422, 325),
            "KHS":  (222, 373),
            "LH":   (288, 568),
            "MC":   (241, 590),
            "MH":   (251, 534),
            "MS":   (312, 291),
            "NPS":  (120, 565),
            "P":    (82, 260),
            "PL":   (258, 438),
            "RGC":  (350, 330),
            "RH":   (401, 320),
            "SCPS": (120, 352),
            "SGMH": (328, 589),
            "SHCC": (307, 360),
            "SRC":  (152, 349),
            "TG":   (237, 352),
            "TH":   (53, 468),
            "TS":   (194, 161),
            "TSC":  (245, 209),
            "TSF":  (298, 237),
            "TSU":  (114, 422),
            "TTC":  (189, 298),
            "TTF":  (224, 243),
            "UP":   (81, 355),
            "VA":   (94, 479)
        }
        self.default_edges = [
            ("AD", "CJ", 31.89),
            ("AD", "SGMH", 29.53),
            ("AF", "TSF", 50.16),
            ("ASC", "TH", 33.94),
            ("B", "CPAC", 73.06),
            ("B", "KHS", 51.31),
            ("B", "PL", 67.68),
            ("B", "SHCC", 126.12),
            ("CC", "TS", 89.19),
            ("CC", "TTC", 116.82),
            ("CC", "TTF", 113.22),
            ("CJ", "ESPS", 104.24),
            ("CPAC", "MH", 70.29),
            ("CPAC", "PL", 79.51),
            ("CPAC", "VA", 103.48),
            ("CP", "SGMH", 57.04),
            ("CY", "TTC", 102.11),
            ("CY", "UP", 72.34),
            ("DBH", "MC", 30.02),
            ("DBH", "MH", 39.05),
            ("E", "CS", 22.02),
            ("E", "EC", 68.62),
            ("ENPS", "CS", 85.45),
            ("ENPS", "EC", 119.85),
            ("ESPS", "ENPS", 38.33),
            ("GAH", "SCPS", 55.23),
            ("GAS", "CS", 52.84),
            ("GAS", "RGC", 54.23),
            ("GF", "AF", 54.63),
            ("H", "GH", 43.01),
            ("HRE", "GAS", 34.06),
            ("KHS", "PL", 74.30),
            ("LH", "AD", 15.65),
            ("LH", "GH", 39.66),
            ("LH", "GH", 39.66),
            ("LH", "MH", 50.25),
            ("MC", "LH", 51.89),
            ("MH", "H", 73.24),
            ("MH", "PL", 96.25),
            ("MS", "RGC", 54.45),
            ("MS", "SHCC", 69.18),
            ("NPS", "GC", 70.38),
            ("NPS", "VA", 89.84),
            ("P", "CC", 64.35),
            ("P", "CY", 23.77),
            ("PL", "EC", 47.68),
            ("PL", "SHCC", 92.11),
            ("RGC", "E", 66.03),
            ("RH", "GAS", 31.02),
            ("RH", "HRE", 21.59),
            ("RH", "RGC", 51.97),
            ("SCPS", "SRC", 32.14),
            ("SHCC", "E", 57.63),
            ("SHCC", "EC", 86.02),
            ("SHCC", "RGC", 52.43),
            ("SRC", "B", 79.08),
            ("SRC", "KHS", 74.00),
            ("TG", "KHS", 25.81),
            ("TG", "SHCC", 70.46),
            ("TG", "TTC", 72.25),
            ("TG", "TSF", 130.18),
            ("TG", "TTF", 109.77),
            ("TH", "GAH", 80.78),
            ("TH", "VA", 42.45),
            ("TS", "GF", 65.15),
            ("TS", "TSC", 70.04),
            ("TSC", "AF", 37.59),
            ("TSC", "TSF", 59.94),
            ("TSC", "TTF", 39.96),
            ("TSF", "MS", 55.79),
            ("TSU", "B", 80.22),
            ("TSU", "CPAC", 106.67),
            ("TSU", "GAH", 42.45),
            ("TSU", "SRC", 82.30),
            ("TTC", "MS", 123.20),
            ("TTC", "SRC", 63.01),
            ("TTF", "TSF", 74.24),
            ("TTF", "TTC", 65.19),
            ("UP", "GAH", 38.05),
            ("UP", "SCPS", 39.12),
            ("VA", "TSU", 60.41),
        ]
        self._build_layout()
        self.animating = False


        self.loaded_text = ""  # for notes search

    def _build_layout(self):
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")
        ttk.Label(header, text="Titan Campus Algorithmic Assistant (TCAA)",
                  font=("Segoe UI", 18, "bold")).pack(side="left")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True)

        self._build_campus_tab()
        self._build_study_tab()
        self._build_notes_tab()
        self._build_about_tab()
    

    # ------------------------------------------------------------------
    # TAB 1: Campus Navigator
    # ------------------------------------------------------------------    
    def _build_campus_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Campus Navigator")

        # LEFT: Inputs
        left = ttk.LabelFrame(tab, text="Inputs", padding=10)
        left.pack(side="left", fill="y")

        # MIDDLE: Canvas / Map
        middle = ttk.LabelFrame(tab, text="Campus Map", padding=10)
        middle.pack(side="left", fill="both", expand=True, padx=10)

        # RIGHT: Output
        right = ttk.LabelFrame(tab, text="Output", padding=10)
        right.pack(side="left", fill="both", expand=True)


        # Input widgets on the LEFT -------------------------------------------------------------------------------------
        buildings = sorted(self.building_positions.keys())

        ttk.Label(left, text="Start Building:").pack(anchor="w")
        self.start_var = tk.StringVar(value=buildings[0])
        self.start_cb = ttk.Combobox(left, textvariable=self.start_var, values=buildings, state="readonly")
        self.start_cb.pack(fill="x", pady=4)

        ttk.Label(left, text="End Building:").pack(anchor="w")
        self.end_var = tk.StringVar(value=buildings[-1])
        self.end_cb = ttk.Combobox(left, textvariable=self.end_var, values=buildings, state="readonly")
        self.end_cb.pack(fill="x", pady=4)

        ttk.Separator(left).pack(fill="x", pady=8)

        ttk.Label(left, text="Choose Algorithm:").pack(anchor="w")
        self.graph_algo_var = tk.StringVar(value="BFS (Fewest Hops)")
        algo_list = ["BFS (Fewest Hops)", "DFS Traversal", "Dijkstra (Shortest Path)", "Prim (MST)"]
        ttk.Combobox(left, textvariable=self.graph_algo_var, values=algo_list, state="readonly").pack(fill="x", pady=4)

        ttk.Button(left, text="Run", command=self.run_graph_algo).pack(fill="x", pady=6)
        ttk.Button(left, text="Reset Output", command=lambda: self.graph_out.delete("1.0", "end")).pack(fill="x")
        
        # Canvas Map on the MIDDLE ---------------------------------------------------------------------------------------
        self.campus_canvas = tk.Canvas(
            middle,
            bg="white",
            width=600,
            height=776
        )

        # Zoom with mouse wheel
        self.campus_canvas.pack(fill="both", expand=True)
        self.campus_canvas.bind("<MouseWheel>", self._on_zoom)

        # Panning with left or middle mouse button
        self.campus_canvas.bind("<ButtonPress-1>", self._start_pan)
        self.campus_canvas.bind("<B1-Motion>", self._do_pan)
        self.campus_canvas.bind("<ButtonPress-3>", self._start_pan)
        self.campus_canvas.bind("<B3-Motion>", self._do_pan)

        # Load Map image
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
        MAP_PATH = PROJECT_ROOT / "assets" / "map_o.png"

        # Verify that the image exists
        if not MAP_PATH.is_file():
            raise FileNotFoundError(
                f"Campus map not found: {MAP_PATH}"
            )

        # Open the image using Pillow
        self.bg_image = Image.open(MAP_PATH)

        # Logical map size (coords + canvas)
        MAP_DISPLAY_WIDTH = 600
        MAP_DISPLAY_HEIGHT = 776

        # Make canvas match coord system
        self.campus_canvas.config(width=MAP_DISPLAY_WIDTH, height=MAP_DISPLAY_HEIGHT)

        # Compute the base scale from original -> display
        w0, h0 = self.bg_image.size  # 2550 x 3300
        self.base_scale = MAP_DISPLAY_WIDTH / w0
        self._resize_background_image()

        # Save positions
        self.building_positions = self.building_positions

        # Draw all nodes on the map
        for label, (x, y) in self.building_positions.items():
            self.draw_node(x, y, label)

        # Draw all edges on the map
        self.edge_items = {}  # (u, v) -> line_id

        for u, v, w in self.default_edges:
            line_id, _, _ = self.draw_edge(u, v, weight=w, color="lightgray", show_label=False)
            # undirected: map both (u,v) and (v,u) to the same line
            self.edge_items[(u, v)] = line_id
            self.edge_items[(v, u)] = line_id        

        # Draw all building nodes
        for label, (x, y) in self.building_positions.items():
            self.draw_node(x, y, label)

        # Build graphs from default_edges
        self.campus_graph_unweighted = {}
        self.campus_graph_weighted = {}

        for u, v, w in self.default_edges:
            # Unweighted
            self.campus_graph_unweighted.setdefault(u, set()).add(v)
            self.campus_graph_unweighted.setdefault(v, set()).add(u)
            # Weighted
            self.campus_graph_weighted.setdefault(u, []).append((v, w))
            self.campus_graph_weighted.setdefault(v, []).append((u, w))

        # Now update scrollregion
        self.campus_canvas.config(scrollregion=self.campus_canvas.bbox("all"))

        # Output Text on the RIGHT ------------------------------------------------------------------------------
        self.graph_out = tk.Text(right, wrap="word", font=("Consolas", 11))
        self.graph_out.pack(fill="both", expand=True)
    
    def draw_node(self, x, y, label, radius=15):
        node_id = self.campus_canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill="#dfe6e9",
            outline="black",
            width=2,
            tags=("node", "content")
        )

        text_id = self.campus_canvas.create_text(
            x, y,
            text=label,
            font=("Consolas", 10, "bold"),
            tags=("label", "content")
        )

        # Maps for later access
        if not hasattr(self, "node_id_to_label"):
            self.node_id_to_label = {}
        if not hasattr(self, "label_to_node_id"):
            self.label_to_node_id = {}

        self.node_id_to_label[node_id] = label
        self.label_to_node_id[label] = node_id

        return node_id, text_id
    
    def draw_edge(self, b1, b2, weight=None, color="gray", width=2, show_label=True):
        # Get original logical positions (600x776 space)
        x1, y1 = self.building_positions[b1]
        x2, y2 = self.building_positions[b2]

        # Draw the edge on screen; it will zoom/pan with tag 'content'
        line_id = self.campus_canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=width,
            tags=("edge", "content")
        )

        # Compute weight from coords if not provided
        if weight is None:
            dx = x2 - x1
            dy = y2 - y1
            weight = math.hypot(dx, dy)

        label_id = None
        if show_label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            label_id = self.campus_canvas.create_text(
                mx, my - 10,
                text=f"{weight:.2f}",
                fill=color,
                font=("Consolas", 9, "bold"),
                tags=("edge_label", "content")
            )

        return line_id, label_id, weight
    
    def _start_pan(self, event):
        # Remember where the drag started
        self.campus_canvas.scan_mark(event.x, event.y)

    def _do_pan(self, event):
        # Drag (move the view) to the new mouse position
        self.campus_canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_zoom(self, event):
        # Zoom from mouse wheel
        if event.delta > 0:
            new_zoom = self.zoom_factor * 1.1
        else:
            new_zoom = self.zoom_factor / 1.1

        if not (self.min_zoom <= new_zoom <= self.max_zoom):
            return

        # Update zoom factor
        scale = new_zoom / self.zoom_factor
        self.zoom_factor = new_zoom

        canvas = self.campus_canvas

        # SCALE CANVAS ITEMS (nodes, lines, text)
        canvas.scale("content", 0, 0, scale, scale)

        # RESIZE BACKGROUND IMAGE
        self._resize_background_image()

        # Expand scroll region
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _resize_background_image(self):
        # Original image stored as self.bg_image
        w, h = self.bg_image.size  # 2550 x 3300

        # Effective scale = base downscale (to 600x776) * current zoom
        effective_scale = self.base_scale * self.zoom_factor

        new_w = int(w * effective_scale)
        new_h = int(h * effective_scale)

        # Resize with Pillow from the ORIGINAL each time
        resized = self.bg_image.resize((new_w, new_h), Image.LANCZOS)

        # Convert to PhotoImage
        self.campus_bg_image = ImageTk.PhotoImage(resized)

        # Replace the background image
        self.campus_canvas.delete("bg")
        self.campus_canvas.create_image(0, 0, image=self.campus_bg_image, anchor="nw", tags="bg")

        # Send image to the back
        self.campus_canvas.tag_lower("bg")

    def _set_node_color(self, label, fill="#dfe6e9", outline="black"):
        if not hasattr(self, "label_to_node_id"):
            return
        node_id = self.label_to_node_id.get(label)
        if node_id is None:
            return
        self.campus_canvas.itemconfigure(node_id, fill=fill, outline=outline)

    def _reset_node_colors(self):
        if not hasattr(self, "label_to_node_id"):
            return
        for label in self.label_to_node_id.keys():
            self._set_node_color(label, fill="#dfe6e9", outline="black")

    def animate_visit_order(self, order, path=None, delay=300):
        # prevent double animations
        self.animating = True
        self._reset_node_colors()

        def step(i):
            if i >= len(order):
                # after visit order, animate final path if given
                if path:
                    self.animate_path(path, delay=300)
                else:
                    self.animating = False
                return

            label = order[i]
            # visited node color
            self._set_node_color(label, fill="#ffeaa7", outline="orange")

            # schedule next step
            self.campus_canvas.after(delay, lambda: step(i + 1))

        step(0)

    def animate_path(self, path, delay=300):
        if not path:
            self.animating = False
            return

        # Reset edges so we only see the current path highlighted
        self._reset_edge_colors()

        self.animating = True

        def step(i):
            if i >= len(path):
                self.animating = False
                return

            label = path[i]
            # highlight node
            self._set_node_color(label, fill="#55efc4", outline="green")

            # from previous node to this one: highlight edge
            if i > 0:
                u = path[i - 1]
                v = path[i]
                self._highlight_edge(u, v, color="#00b894", width=4)

            self.campus_canvas.after(delay, lambda: step(i + 1))

        step(0)

    def _draw_mst_edges(self, mst_edges):
        # Remove any old MST visualization
        self._clear_mst_edges()

        for u, v, w in mst_edges:
            if u not in self.building_positions or v not in self.building_positions:
                continue

            x1, y1 = self.building_positions[u]
            x2, y2 = self.building_positions[v]

            # Draw highlighted MST edge
            self.campus_canvas.create_line(
                x1, y1, x2, y2,
                fill="#00b894",           # green-ish
                width=4,                    # thicker than normal edges
                tags=("edge", "content", "mst_edge")
            )
    
    def _clear_mst_edges(self):
        for item_id in self.campus_canvas.find_withtag("mst_edge"):
            self.campus_canvas.delete(item_id)

    def _highlight_edge(self, u, v, color="#00b894", width=4):
        if not hasattr(self, "edge_items"):
            return

        line_id = self.edge_items.get((u, v))
        if line_id is None:
            return

        self.campus_canvas.itemconfigure(line_id, fill=color, width=width)

    def _reset_edge_colors(self):
        if not hasattr(self, "edge_items"):
            return

        # Use set(...) so we don't reset the same line twice
        for line_id in set(self.edge_items.values()):
            self.campus_canvas.itemconfigure(line_id, fill="lightgray", width=2)


    def run_graph_algo(self):
        if getattr(self, "animating", False):
            self.graph_out.insert("end", "Animation in progress. Please wait...\n")
            self.graph_out.see("end")
            return
        
        self._reset_node_colors()
        self._reset_edge_colors()
        self._clear_mst_edges()
    
        algo = self.graph_algo_var.get()
        start = self.start_var.get()
        end = self.end_var.get()

        self.graph_out.insert("end", f"\n=== {algo} ===\n")
        self.graph_out.insert("end", f"Start: {start} | End: {end}\n")

        # --- BFS: fewest hops ---
        if algo.startswith("BFS"):
            if bfs_shortest_paths is None or reconstruct_path is None:
                self.graph_out.insert("end", "Error: bfs_demo.py not found or missing functions.\n")
                return

            dist, parent, order = bfs_shortest_paths(self.campus_graph_unweighted, start)
            path = reconstruct_path(parent, start, end)

            self.graph_out.insert("end", f"BFS visit order: {order}\n")
            if path:
                self.graph_out.insert("end", f"Shortest path (fewest hops) {start} -> {end}: {path}\n")
                self.graph_out.insert("end", f"Hops: {dist[end]}\n")
            else:
                self.graph_out.insert("end", f"No path found from {start} to {end}.\n")
            
            # Animate BFS: first visit order, then final shortest path
            if path:
                self.animate_visit_order(order, path=path, delay=80)
            else:
                self.animate_visit_order(order, path=None, delay=80)


        # --- DFS: traversal order from start ---
        elif algo.startswith("DFS"):
            order = dfs_traversal(self.campus_graph_unweighted, start)
            self.graph_out.insert("end", f"DFS visit order from {start}: {order}\n")

            path  = dfs_path(self.campus_graph_unweighted, start, end)
            if path:
                self.graph_out.insert("end", f"One DFS path {start} -> {end}: {path}\n")
                self.graph_out.insert("end", "(DFS path is NOT shortest — it's just the first found.)\n")
            else:
                self.graph_out.insert("end", f"No DFS path found from {start} to {end}.\n")

            # Animate DFS: any path
            if order:
                # Show traversal first
                def after_order():
                    if path:
                        self.animate_path(path, delay=250)
                self.animate_visit_order(order, path=None, delay=80)
                
                if path:
                    self.campus_canvas.after(len(order) * 90, after_order)

        # --- Dijkstra: weighted shortest path ---
        elif algo.startswith("Dijkstra"):
            # If the algorithm file didn't load
            if dijkstra is None or rebuild_path is None:
                self.graph_out.insert("end", "Error: dijkstra function not available.\n")
                return

            # Run Dijkstra
            dist, parent = dijkstra(self.campus_graph_weighted, start)

            # Extract distance to 'end'
            d = dist.get(end, float("inf"))

            if d == float("inf"):
                self.graph_out.insert("end", f"No weighted path found from {start} to {end}.\n")
            else:
                # Rebuild the actual shortest path
                path = rebuild_path(parent, end)

                # Number of edges in the path
                hops = len(path) - 1 if path else 0

                self.graph_out.insert("end", f"Weighted shortest path {start} -> {end}: {path}\n")
                self.graph_out.insert("end", f"Total distance: {d:.2f}\n")
                self.graph_out.insert("end", f"Hops in path: {hops}\n")

                # Animate the final path
                self.animate_path(path, delay=300)

        # --- Prim: MST from start ---
        elif algo.startswith("Prim"):
            if prim is None:
                self.graph_out.insert("end", "Error: prim_demo.py not found or missing function.\n")
                return

            mst_edges, cost = prim(self.campus_graph_weighted, start)
            self.graph_out.insert("end", f"Minimum Spanning Tree starting at {start}:\n")
            for (u, v, w) in mst_edges:
                self.graph_out.insert("end", f"  {u} -- {v} (w={w})\n")
            self.graph_out.insert("end", f"Total MST cost: {cost}\n")
            self._draw_mst_edges(mst_edges)

        else:
            self.graph_out.insert("end", "Unknown algorithm selection.\n")

        self.graph_out.insert("end", "\n")
        self.graph_out.see("end")


    # ------------------------------------------------------------------
    # TAB 2: Study Planner (Greedy + Knapsack placeholders)
    # ------------------------------------------------------------------
    def _build_study_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Study Planner")

        left = ttk.LabelFrame(tab, text="Add Task", padding=10)
        left.pack(side="left", fill="y", expand=False)

        middle = ttk.LabelFrame(tab, text="Tasks", padding=10)
        middle.pack(side="left", fill="both", expand=True)

        right = ttk.LabelFrame(tab, text="Output", padding=10)
        right.pack(side="right", fill="both", expand=False)

        ttk.Label(left, text="Task Name").pack(anchor="w")
        self.task_name = tk.StringVar()
        ttk.Entry(left, textvariable=self.task_name).pack(fill="x", pady=3)

        ttk.Label(left, text="Time (hours)").pack(anchor="w")
        self.task_time = tk.StringVar(value=1.0)
        self.task_time_spin = ttk.Spinbox(
            left,
            from_=0.25,      # minimum
            to=24.0,         # maximum
            increment=0.25,  # step (15 minutes)
            textvariable=self.task_time,
            format="%.2f"
        )
        self.task_time_spin.pack(fill="x", pady=3)


        ttk.Label(left, text="Value (importance)").pack(anchor="w")
        self.task_value = tk.StringVar(value="5")
        self.value_combo = ttk.Combobox(
            left,
            textvariable=self.task_value,
            values=[str(i) for i in range(0, 11)],
            state="readonly"
        )
        self.value_combo.pack(fill="x", pady=3)

        ttk.Button(left, text="Add Task", command=self.add_task).pack(fill="x", pady=6)

        ttk.Separator(left).pack(fill="x", pady=8)

        ttk.Label(left, text="Available Time (hours)").pack(anchor="w")
        self.avail_time = tk.StringVar(value=4.0)
        self.avail_time_spin = ttk.Spinbox(
            left,
            from_=0.25,
            to=24.0,
            increment=0.25,
            textvariable=self.avail_time,
            format="%.2f"
        )
        self.avail_time_spin.pack(fill="x", pady=3)


        self.study_algo_var = tk.StringVar(value="Greedy Scheduler")
        ttk.Combobox(left, textvariable=self.study_algo_var,
                     values=["Greedy Scheduler", "DP Knapsack Optimal", "Compare Both"],
                     state="readonly").pack(fill="x", pady=4)

        ttk.Button(left, text="Run Planner", command=self.run_study_planner).pack(fill="x", pady=6)
        ttk.Button(left, text="Clear Tasks", command=self.clear_tasks).pack(fill="x")

        self.task_listbox = tk.Listbox(middle, font=("Consolas", 11))
        self.task_listbox.pack(fill="both", expand=True)

        self.study_out = tk.Text(right, wrap="word", font=("Consolas", 11))
        self.study_out.pack(fill="both", expand=True)

        self.tasks = []  # list of dicts

    def add_task(self):
        name = self.task_name.get().strip()
        if not name:
            messagebox.showwarning("Missing name", "Enter a task name.")
            return

        # Get raw strings from the widgets
        t_str = self.task_time.get().strip()
        v_str = self.task_value.get().strip()

        try:
            t = float(t_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Time must be a numeric value.")
            return

        try:
            v = int(v_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Value must be an integer from 0 to 10.")
            return

        if t <= 0:
            messagebox.showwarning("Invalid Time", "Time must be greater than 0.")
            return

        if v < 0:
            messagebox.showwarning("Invalid Value", "Value cannot be negative.")
            return


        self.tasks.append({"name": name, "time": t, "value": v})
        self.task_listbox.insert("end", f"{name} | time={t} | value={v}")

        # Reset fields
        self.task_name.set("")
        self.task_time.set(1.0)
        self.task_value.set(5)


    def clear_tasks(self):
        self.tasks.clear()
        self.task_listbox.delete(0, "end")
        self.study_out.delete("1.0", "end")

    def greedy_scheduler(self, tasks, cap):
        tasks_sorted = sorted(tasks, key=lambda x: x["value"] / x["time"], reverse=True)
        chosen, used, score = [], 0.0, 0

        for task in tasks_sorted:
            if used + task["time"] <= cap:
                chosen.append(task)
                used += task["time"]
                score += task["value"]

        return chosen, used, score

    def knapsack_scheduler(self, tasks, cap, granularity=0.25):
        if cap <= 0 or not tasks:
            return [], 0.0, 0

        # Convert hours to discrete units
        W = int(cap / granularity + 1e-9)
        n = len(tasks)

        weights = [int(t["time"] / granularity + 1e-9) for t in tasks]
        values = [t["value"] for t in tasks]

        # dp[i][w] = max value using first i items with capacity w
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            wt = weights[i - 1]
            val = values[i - 1]
            for w in range(W + 1):
                # option 1: skip
                best = dp[i - 1][w]
                # option 2: take (if fits)
                if wt <= w:
                    cand = dp[i - 1][w - wt] + val
                    if cand > best:
                        best = cand
                dp[i][w] = best

        # Reconstruct chosen tasks
        chosen_indices = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                # task i-1 was taken
                chosen_indices.append(i - 1)
                w -= weights[i - 1]

        chosen_indices.reverse()
        chosen = [tasks[i] for i in chosen_indices]

        used_time = sum(t["time"] for t in chosen)
        total_value = dp[n][W]

        return chosen, used_time, total_value

    def run_study_planner(self):
        if not self.tasks:
            self.study_out.insert("end", "No tasks added.\n")
            return

        # Clear output before each run
        self.study_out.delete("1.0", "end")

        # Validate available time
        try:
            cap = float(self.avail_time.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Available time must be a number.")
            return

        if cap <= 0:
            messagebox.showerror("Invalid Time", "Available time must be greater than 0.")
            return

        algo = self.study_algo_var.get()
        self.study_out.insert("end", f"--- {algo} (cap={cap} hours) ---\n\n")

        if algo == "Greedy Scheduler":
            chosen, used, score = self.greedy_scheduler(self.tasks, cap)
            self._print_schedule("Greedy", chosen, used, score)

        elif algo == "DP Knapsack Optimal":
            chosen, used, score = self.knapsack_scheduler(self.tasks, cap)
            self._print_schedule("DP (Optimal)", chosen, used, score)

        else:  # Compare Both
            g_chosen, g_used, g_score = self.greedy_scheduler(self.tasks, cap)
            d_chosen, d_used, d_score = self.knapsack_scheduler(self.tasks, cap)

            self._print_schedule("Greedy", g_chosen, g_used, g_score)
            self._print_schedule("DP (Optimal)", d_chosen, d_used, d_score)



    def _print_schedule(self, label, chosen, used, score):
        self.study_out.insert("end", f"{label} chose:\n")
        for task in chosen:
            self.study_out.insert("end", f"  - {task['name']} (t={task['time']}, v={task['value']})\n")
        self.study_out.insert("end", f"Total time: {used} hours | Total value: {score}\n\n")

    # ------------------------------------------------------------------
    # TAB 3: Notes Search Engine (file load + string search)
    # ------------------------------------------------------------------
    def _build_notes_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="Notes Search Engine")

        left = ttk.LabelFrame(tab, text="Load File", padding=10)
        left.pack(side="left", fill="both")

        right = ttk.LabelFrame(tab, text="Output", padding=10)
        right.pack(side="right", fill="both", expand=True)

        ttk.Button(left, text="Open TXT/PDF/DOCX", command=self.open_notes_file).pack(fill="x", pady=4)

        self.file_label = ttk.Label(left, text="No file loaded", wraplength=220)
        self.file_label.pack(fill="x", pady=6)

        ttk.Label(left, text="Previously loaded files:").pack(anchor="w", pady=(4, 0))
        self.notes_file_var = tk.StringVar()
        self.notes_file_combo = ttk.Combobox(
            left,
            textvariable=self.notes_file_var,
            state="readonly",
            values=[],
            width=30
        )
        self.notes_file_combo.pack(fill="x", pady=4)
        self.notes_file_combo.bind("<<ComboboxSelected>>", self._on_notes_file_selected)

        ttk.Label(left, text="Pattern to search:").pack(anchor="w")
        self.pattern_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.pattern_var).pack(fill="x", pady=4)

        self.search_algo_var = tk.StringVar(value="Naive")
        ttk.Combobox(left, textvariable=self.search_algo_var,
                    values=["Naive", "Rabin–Karp", "KMP", "ALL (Compare)"],
                    state="readonly").pack(fill="x", pady=4)

        ttk.Button(left, text="Search", command=self.run_search).pack(fill="x", pady=6)

        self.notes_out = tk.Text(right, wrap="word", font=("Consolas", 11))
        self.notes_out.pack(fill="both", expand=True)

    def _on_notes_file_selected(self, event=None):
        selected_name = self.notes_file_var.get()
        if not selected_name:
            return

        # find the corresponding file info
        for info in self.notes_files:
            if info["name"] == selected_name:
                self.loaded_text = info["text"]
                self.file_label.config(text=info["name"])
                self.notes_out.delete("1.0", "end")
                self.notes_out.insert(
                    "end",
                    f"Switched to {info['name']} ({len(info['text'])} characters loaded).\n"
                )
                break

    def open_notes_file(self):
        path = filedialog.askopenfilename(
            title="Open notes",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx")
            ],
        )
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        text = ""

        try:
            if ext == ".txt":
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()

            elif ext == ".pdf":
                text = ""
                with open(path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text() or ""
                        text += page_text + "\n"

            elif ext == ".docx":
                doc = Document(path)
                parts = [para.text for para in doc.paragraphs]
                text = "\n".join(parts)

            else:
                messagebox.showerror("Unsupported", "Only TXT, PDF, DOCX supported.")
                return

            name = os.path.basename(path)
            existing = next((f for f in self.notes_files if f["path"] == path), None)
            if existing:
                existing["text"] = text
                existing["name"] = name
            else:
                self.notes_files.append({"name": name, "path": path, "text": text})

            names = [f["name"] for f in self.notes_files]
            self.notes_file_combo["values"] = names
            self.notes_file_var.set(name)  # select current file

            self.loaded_text = text
            self.file_label.config(text=name)

            self.notes_out.delete("1.0", "end")
            self.notes_out.insert("end", f"Loaded {len(text)} characters from {name}.\n")

        except Exception as e:
            messagebox.showerror("Error loading file", str(e))


    def run_search(self):
        pattern = self.pattern_var.get()
        text = getattr(self, "loaded_text", "")

        # basic validation
        if not text:
            self.notes_out.insert("end", "Load a file first.\n")
            return

        if not pattern:
            self.notes_out.insert("end", "Enter a pattern.\n")
            return

        algo = self.search_algo_var.get()
        self.notes_out.insert("end", f"\n--- Searching for '{pattern}' with {algo} ---\n")

        def timed(run_fn):
            start = time.perf_counter()
            res = run_fn()
            end = time.perf_counter()
            return res, (end - start)

        def safe_call(fn, label):
            if fn is None:
                return [], None, f"{label} implementation not found (import failed)."
            res, t_sec = timed(lambda: fn(text, pattern))
            return res, t_sec, None

        if algo == "Naive":
            res, t_sec, err = safe_call(naive_string_match, "Naive")
            self._print_search_result("Naive", res, t_sec, err)

        elif algo == "Rabin–Karp":
            res, t_sec, err = safe_call(rabin_karp, "Rabin–Karp")
            self._print_search_result("Rabin–Karp", res, t_sec, err)

        elif algo == "KMP":
            res, t_sec, err = safe_call(kmp_search, "KMP")
            self._print_search_result("KMP", res, t_sec, err)

        else:  # ALL (Compare)
            results = []

            for fn, label in [
                (naive_string_match, "Naive"),
                (rabin_karp, "Rabin–Karp"),
                (kmp_search, "KMP"),
            ]:
                res, t_sec, err = safe_call(fn, label)
                self._print_search_result(label, res, t_sec, err)

                if err is None and t_sec is not None:
                    results.append((label, t_sec))

            # Determine fastest
            if results:
                fastest_label, fastest_time = min(results, key=lambda x: x[1])
                self.notes_out.insert(
                    "end",
                    f"Fastest Algorithm: {fastest_label} ({fastest_time:.6f}s)\n"
                )
            else:
                self.notes_out.insert(
                    "end",
                    "No algorithms ran successfully; cannot determine fastest.\n"
                )

    def _print_search_result(self, label, res, t_sec, err):
        if err:
            self.notes_out.insert("end", f"{label}: {err}\n")
            return

        count = len(res)
        if count == 0:
            self.notes_out.insert("end", f"{label}: no matches. time={t_sec:.6f}s\n")
        else:
            # show only the first few indices to avoid huge spam
            preview = res[:20]
            more = " ..." if count > 20 else ""
            self.notes_out.insert(
                "end",
                f"{label}: {count} matches at indices {preview}{more}\n"
            )
            self.notes_out.insert("end", f"{label}: time={t_sec:.6f}s\n\n")

    # ------------------------------------------------------------------
    # TAB 4: About / Info
    # ------------------------------------------------------------------
    def _build_about_tab(self):
        tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(tab, text="About / Info")

        text = tk.Text(tab, wrap="word")
        text.pack(fill="both", expand=True)

        about_msg = (
            "Titan Campus Algorithmic Assistant (TCAA)\n"
            "-----------------------------------------\n"
            "Modules Implemented:\n"
            "1) Campus Navigator  - BFS, DFS, Dijkstra, Prim MST\n"
            "2) Study Planner     - Greedy Scheduling vs DP Knapsack\n"
            "3) Notes Search      - Naive, Rabin-Karp, KMP + timing comparison\n\n"

            "Big-O Complexity Summary:\n"
            "- BFS (shortest unweighted path):     Time O(V + E),   Space O(V)\n"
            "- DFS (traversal / any path):         Time O(V + E),   Space O(V)\n"
            "- Dijkstra (min-heap):                Time O(E log V), Space O(V + E)\n"
            "- Prim's MST (min-heap):              Time O(E log V), Space O(V + E)\n"
            "- Greedy Task Scheduling:             Time O(n log n), Space O(1-n)\n"
            "- DP Knapsack Scheduler:              Time O(n·T),     Space O(n·T)\n"
            "- Naive String Match:                 Time O(n·m),     Space O(1)\n"
            "- KMP String Matching:                Time O(n + m),   Space O(m)\n"
            "- Rabin-Karp:                         Avg O(n + m),    Space O(1),   Worst O(n·m)\n\n"

            "P vs NP Reflection:\n"
            "P is the class of problems solvable in polynomial time. Many algorithms in TCAA—\n"
            "such as BFS, DFS, Dijkstra, Prim, and KMP—run efficiently and are firmly within P.\n\n"
            "NP is the class of problems whose solutions can be \"verified\" in polynomial time.\n\n"

            "Some problems, like the Knapsack problem used in our Study Planner, are NP-complete:\n"
            "    - There is no known polynomial-time algorithm that solves all instances optimally.\n"
            "    - Our Dynamic Programming scheduler is a pseudo-polynomial solution: O(n·T).\n"
            "      It is efficient only when T (available time capacity) is reasonably small.\n\n"
            "This illustrates a real-world idea: when a problem is NP-complete, applications combine\n"
            "heuristics (Greedy) with exact methods (DP) to balance speed and optimality.\n"
            "TCAA demonstrates both polynomial-time algorithms and algorithms related to NP-hard\n"
            "optimization, giving a practical contrast between P and NP in one system.\n"
        )

        text.insert("1.0", about_msg)
        text.config(state="disabled")


if __name__ == "__main__":
    app = TCAAApp()
    app.mainloop()
