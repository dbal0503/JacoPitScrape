import os
import re
from models.models import Project, Package, JavaClass
from utils.complexity import extract_class_complexity, has_complexity_data
from utils.mutation import extract_mutation_scores, has_mutation_data

def extract_package_from_path(file_path):
    """Extract package name from the file path"""
    parts = file_path.split(os.sep)
    package_path = []
    
    found_org = False
    for part in parts:
        if part == "index.html":
            continue
        # If the package is found or the part starts with org, add the part to the package path
        if found_org or part.startswith("org."):
            package_path.append(part)
            found_org = True
        elif part == "org":
            package_path.append(part)
            found_org = True
            
    if not package_path:
        for part in parts:
            if part == "index.html":
                continue
            if re.match(r'^[a-z]+(\.[a-z]+)+$', part):
                return part
        
        return os.path.basename(os.path.dirname(file_path))
    
    package_name = ".".join(package_path)
    return package_name.replace(".index.html", "")

def extract_project_name(directory):
    # Extract the project name from the directory path, the project name is the directory name
    path_parts = directory.rstrip(os.sep).split(os.sep)
    return path_parts[-1]

def find_jacoco_index_files(directory):
    # Find all JaCoCo index.html files in the directory
    jacoco_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        if "index.html" in filenames:
            file_path = os.path.join(dirpath, "index.html")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if "JaCoCo" in content and has_complexity_data(content):
                        jacoco_files.append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return jacoco_files

def find_pit_index_files(directory):
    # Find all PIT index.html files in the directory
    pit_files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        if "index.html" in filenames:
            file_path = os.path.join(dirpath, "index.html")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if has_mutation_data(content):
                        pit_files.append(file_path)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    return pit_files

def process_jacoco_reports(directory, projects):
    # Process JaCoCo reports for complexity data
    # Every jacoco report has an index.html at the project level and at every package level
    jacoco_files = find_jacoco_index_files(directory)
    
    for file_path in jacoco_files:
        project_name = extract_project_name(directory)
        package_name = extract_package_from_path(file_path)
        # Extract packages from the file path
        
        if project_name not in projects:
            # If the project is not in the projects dictionary, create a new project
            projects[project_name] = Project(project_name)
        
        project = projects[project_name]
        # If the package is not in the project, create a new package
        package = project.add_package(package_name)
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                # Read the content of the file
                content = file.read()
                # Extract the complexity data from the content
                complexity_data = extract_class_complexity(content)
                
                # Add the complexity data to the package
                for class_name, complexity in complexity_data.items():
                    # Add the class name and complexity to the package
                    package.add_class(class_name, complexity=complexity)
        except Exception as e:
            print(f"Error processing JaCoCo file {file_path}: {e}")
    
    return projects

def process_pit_reports(directory, projects):
    # Process PIT reports for mutation scores
    # Same exact process as JaCoCo reports refer to the comments in process_jacoco_reports for more information
    pit_files = find_pit_index_files(directory)
    
    for file_path in pit_files:
        project_name = extract_project_name(directory)
        package_name = extract_package_from_path(file_path)
        
        if project_name not in projects:
            projects[project_name] = Project(project_name)
        
        project = projects[project_name]
        package = project.add_package(package_name)
        
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                mutation_data = extract_mutation_scores(content)
                
                for class_name, mutation_score in mutation_data.items():
                    package.add_class(class_name, mutation_score=mutation_score)
        except Exception as e:
            print(f"Error processing PIT file {file_path}: {e}")
    
    return projects

def process_reports(directory):
    # Process all reports in the directory
    projects = {}
    
    projects = process_jacoco_reports(directory, projects)
    
    projects = process_pit_reports(directory, projects)
    
    # If a class does not contain both complexity and mutation score, it is removed
    for project in projects.values():
        project.cleanup_incomplete_classes()
    
    return projects 