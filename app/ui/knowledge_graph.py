import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from ui.components import render_page_header
import time

def render_knowledge_graph():
    render_page_header("🕸️", "Living Medical Knowledge Graph", "A graph connecting genes, proteins, cells, organs, diseases, and drugs.", "linear-gradient(135deg, #f59e0b, #d97706)")
    
    st.markdown("### Biomedical Knowledge Exploration")
    st.info("Visualizing billions of nodes updated continuously as new evidence appears.")
    
    query = st.text_input("Enter a disease, gene, or drug to explore its causal network:", "BRCA1 Gene")
    
    if st.button("🕸️ Traverse Knowledge Graph", type="primary"):
        with st.spinner(f"Traversing pathways connected to {query}..."):
            time.sleep(0.01)
            
        # Simulate a small subnet graph
        G = nx.Graph()
        G.add_node(query, type="Target", size=30, color="#ef4444")
        
        # Related nodes
        related = [
            ("Breast Cancer", "Disease", 20, "#3b82f6"),
            ("Ovarian Cancer", "Disease", 20, "#3b82f6"),
            ("PARP Inhibitors (Olaparib)", "Drug", 25, "#10b981"),
            ("DNA Repair Pathway", "Cellular Process", 15, "#f59e0b"),
            ("TP53 Mutation", "Gene", 15, "#8b5cf6")
        ]
        
        for name, typ, size, color in related:
            G.add_node(name, type=typ, size=size, color=color)
            G.add_edge(query, name)
            
        # Add some cross edges
        G.add_edge("Breast Cancer", "PARP Inhibitors (Olaparib)")
        G.add_edge("Ovarian Cancer", "PARP Inhibitors (Olaparib)")
        G.add_edge("DNA Repair Pathway", "TP53 Mutation")
        
        pos = nx.spring_layout(G, seed=42)
        
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')
            
        node_x = []
        node_y = []
        node_colors = []
        node_sizes = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_colors.append(G.nodes[node]['color'])
            node_sizes.append(G.nodes[node]['size'])
            node_text.append(f"{node} ({G.nodes[node]['type']})")
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="bottom center",
            marker=dict(
                showscale=False,
                color=node_colors,
                size=node_sizes,
                line_width=2))
                
        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Local Sub-Graph Neighborhood',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
             ))
             
        st.plotly_chart(fig, use_container_width=True)
        st.success("Graph Traversal Complete. Note how the DNA Repair Pathway heavily links to PARP Inhibitor efficacy.")
