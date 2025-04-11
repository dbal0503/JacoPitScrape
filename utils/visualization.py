import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats 

def ensure_graph_dir(project_dir=None):
    # Ensure the graphs directory exists in the current working directory
    graph_dir = os.path.join(os.getcwd(), "graphs")
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    return graph_dir

def create_scatter_plot(projects):
    # Create a scatter plot of complexity vs mutation score
    complexities = []
    mutation_scores = []
    labels = []  
    
    for project_name, project in projects.items():
        for package_name, package in project.packages.items():
            for class_name, java_class in package.classes.items():
                complexities.append(java_class.complexity)
                mutation_scores.append(java_class.mutation_score)
                labels.append(f"{package_name}.{class_name}")
    
    graph_dir = ensure_graph_dir()
    
    plt.figure(figsize=(12, 8))
    plt.scatter(complexities, mutation_scores, alpha=0.6)
    
    if complexities:
        z = np.polyfit(complexities, mutation_scores, 1)
        p = np.poly1d(z)
        plt.plot(complexities, p(complexities), "r--", alpha=0.8)
        
        correlation, p_value = stats.pearsonr(complexities, mutation_scores)
        plt.text(0.05, 0.95, f"Correlation: {correlation:.2f}", transform=plt.gca().transAxes)
        plt.text(0.05, 0.90, f"p-value: {p_value:.4f}", transform=plt.gca().transAxes)
    
    plt.xlabel('Cyclomatic Complexity')
    plt.ylabel('Mutation Score (%)')
    plt.title('Mutation Score vs Cyclomatic Complexity')
    plt.grid(True, alpha=0.3)
    
    scatter_path = os.path.join(graph_dir, "complexity_vs_mutation.png")
    plt.savefig(scatter_path)
    plt.close()
    
    print(f"Scatter plot saved to {scatter_path}")
    return scatter_path


def create_table_plot(projects):
    # Create a visual table of complexity and mutation scores
    graph_dir = ensure_graph_dir()
    
    data = []
    
    for project_name, project in projects.items():
        for package_name, package in project.packages.items():
            for class_name, java_class in package.classes.items():
                short_package = package_name.split('.')[-2:] if '.' in package_name else [package_name]
                short_package = '.'.join(short_package)
                
                data.append([
                    short_package,
                    class_name,
                    java_class.complexity,
                    java_class.mutation_score
                ])
    
    data.sort(key=lambda x: x[2], reverse=True)
    
    data = data[:20]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(
        cellText=[[str(item) for item in row] for row in data],
        colLabels=['Package', 'Class', 'Complexity', 'Mutation Score (%)'],
        loc='center',
        cellLoc='center'
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    for i in range(len(data)):
        complexity = data[i][2]
        complexity_cell = table[(i+1, 2)]
        if complexity > 20:
            complexity_cell.set_facecolor("#ffcccc")  # Red for high complexity
        elif complexity > 10:
            complexity_cell.set_facecolor("#ffffcc")  # Yellow for medium complexity
        else:
            complexity_cell.set_facecolor("#ccffcc")  # Green for low complexity
            
        mutation = data[i][3]
        mutation_cell = table[(i+1, 3)]
        if mutation < 50:
            mutation_cell.set_facecolor("#ffcccc")  # Red for low mutation score
        elif mutation < 80:
            mutation_cell.set_facecolor("#ffffcc")  # Yellow for medium mutation score
        else:
            mutation_cell.set_facecolor("#ccffcc")  # Green for high mutation score
    
    plt.title('Top 20 Most Complex Classes', fontsize=14)
    
    table_path = os.path.join(graph_dir, "complexity_table.png")
    plt.savefig(table_path, bbox_inches='tight')
    plt.close()
    
    print(f"Table plot saved to {table_path}")
    return table_path

def create_histogram(projects):
    # Create histograms of complexity and mutation score distributions
    graph_dir = ensure_graph_dir()
    
    complexities = []
    mutation_scores = []
    
    for project_name, project in projects.items():
        for package_name, package in project.packages.items():
            for class_name, java_class in package.classes.items():
                complexities.append(java_class.complexity)
                mutation_scores.append(java_class.mutation_score)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Create a histogram of the complexity distribution
    ax1.hist(complexities, bins=10, alpha=0.7, color='blue')
    ax1.set_title('Distribution of Cyclomatic Complexity')
    ax1.set_xlabel('Complexity')
    ax1.set_ylabel('Number of Classes')
    
    # Create a histogram of the mutation score distribution 
    ax2.hist(mutation_scores, bins=10, alpha=0.7, color='green')
    ax2.set_title('Distribution of Mutation Scores')
    ax2.set_xlabel('Mutation Score (%)')
    ax2.set_ylabel('Number of Classes')
    
    plt.tight_layout()
    
    hist_path = os.path.join(graph_dir, "histograms.png")
    plt.savefig(hist_path)
    plt.close()
    
    print(f"Histograms saved to {hist_path}")
    return hist_path

def generate_visualizations(projects):
    # Create a scatter plot of complexity vs mutation score
    scatter_path = create_scatter_plot(projects)
    # Create a visual table of complexity and mutation scores
    table_path = create_table_plot(projects)
    # Create histograms of complexity and mutation score distributions
    hist_path = create_histogram(projects)
    
    return {
        'scatter': scatter_path,
        'table': table_path,
        'histogram': hist_path
    } 