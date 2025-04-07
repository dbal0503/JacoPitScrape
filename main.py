"""
David Ballard: 40262526
Anthony El-Khoury: 40262893

This script is used to process JACOCO and PIT reports for Java projects. 
This is used on projects from the defects4j project https://github.com/rjust/defects4j

The output is a csv with the mutation score and complexity for each class.

The script also generates graphs of the complexity and mutation score distributions.

The graphs generated are:
- A scatter plot of complexity vs mutation score
- A visual table of complexity and mutation scores
- Histograms of the complexity and mutation score distributions

Date: 2025-04-07
"""
import os
import argparse
from utils.report_processor import process_reports
from utils.report_display import display_results, export_to_csv
from utils.visualization import generate_visualizations

def parse_arguments():
    # Parse command-line arguments csv and graphs are optional, csv path is required
    parser = argparse.ArgumentParser(description="Process HTML reports for Java projects.")
    parser.add_argument("directory", help="Path to the directory containing the HTML reports")
    parser.add_argument("--csv", help="Export results to a CSV file", dest="csv_file")
    parser.add_argument("--graphs", action="store_true", help="Generate graphs and visualizations")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        return
    
    print(f"Processing reports in: {args.directory}")
    # Process reports and return a dictionary of projects given a root directory
    # Keys are formed from each project found in the root directory
    # Each project is an aggregate of packages found in the project
    # Each package is an aggregate of classes found in the package
    # Refer to the models.py as well as the artifacts for more information regarding the data model
    projects = process_reports(args.directory)
    
    display_results(projects)
    
    if args.csv_file:
        export_to_csv(projects, args.csv_file)
    
    if args.graphs:
        print("\nGenerating visualizations...")
        generate_visualizations(projects)
        print("Visualizations generated in the 'graphs' directory in the current working directory.")

if __name__ == "__main__":
    main()