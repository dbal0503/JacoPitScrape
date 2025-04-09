def display_results(projects):
    # Prints results to CLI
    if not projects:
        print("No reports found or no classes with both complexity and mutation score metrics.")
        return
    total_classes = 0
    all_complexities = []
    all_mutation_scores = []
    
    for project_name, project in projects.items():
        print(f"\nProject: {project_name}")
        project_classes = 0
        
        # If there are no packages with complete metrics, skip the project
        if not project.packages:
            print("  No packages with complete metrics found")
            continue
        
        # Print the packages in the project
        for package_name in sorted(project.packages.keys()):
            package = project.packages[package_name]
            # Print the package name
            print(f"  Package: {package.name}")
            package_classes = 0
            # Print the classes in the package
            for class_name in sorted(package.classes.keys()):
                java_class = package.classes[class_name]
                print(f"    Class: {class_name}")
                print(f"      Complexity: {java_class.complexity}")
                print(f"      Mutation Score: {java_class.mutation_score}%")
                
                package_classes += 1
                all_complexities.append(java_class.complexity)
                all_mutation_scores.append(java_class.mutation_score)
                
            print(f"  Total classes in package: {package_classes}")
            project_classes += package_classes
            
        print(f"Total classes in project: {project_classes}")
        total_classes += project_classes
    
    if all_complexities and all_mutation_scores:
        print_summary_statistics(total_classes, all_complexities, all_mutation_scores)

# Prints summary statistics to CLI
def print_summary_statistics(total_classes, complexities, mutation_scores):
    # Calculate the average complexity and mutation score
    avg_complexity = sum(complexities) / len(complexities)
    avg_mutation = sum(mutation_scores) / len(mutation_scores)
    # Print the summary statistics
    print("\n--- Summary Statistics ---")
    print(f"Total classes with both metrics: {total_classes}")
    print(f"Average complexity: {avg_complexity:.2f}")
    print(f"Average mutation score: {avg_mutation:.2f}%")
    print(f"Highest complexity: {max(complexities)}")
    print(f"Lowest complexity: {min(complexities)}")
    print(f"Highest mutation score: {max(mutation_scores)}%")
    print(f"Lowest mutation score: {min(mutation_scores)}%")

def export_to_csv(projects, output_file):
    # Export the analysis results to a CSV file
    import csv
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Project', 'Package', 'Class', 'Complexity', 'Mutation Score'])
        
        for project_name, project in projects.items():
            for package_name, package in project.packages.items():
                for class_name, java_class in package.classes.items():
                    writer.writerow([
                        project_name,
                        package.name,
                        class_name,
                        java_class.complexity,
                        java_class.mutation_score
                    ])
    
    print(f"Results exported to {output_file}") 