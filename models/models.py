class JavaClass:
    def __init__(self, name: str, complexity: int = 0, mutation_score: int = 0):
        self._name = name
        self._complexity = complexity
        self._mutation_score = mutation_score
    
    @property
    def name(self):
        return self._name
    
    @property
    def complexity(self):
        return self._complexity
    
    @complexity.setter
    def complexity(self, value):
        self._complexity = value
    
    @property
    def mutation_score(self):
        return self._mutation_score
    
    @mutation_score.setter
    def mutation_score(self, value):
        self._mutation_score = value

class Package:
    def __init__(self, name: str):
        self._name = name # Name of the package
        self.classes = {} # Dictionary of {class_name : JavaClass}
    
    @property
    def name(self):
        return self._name
    
    def add_class(self, class_name: str, complexity: int = 0, mutation_score: int = -1):
        if class_name.startswith("org.") or class_name.startswith("com."):
            return
        if class_name in self.classes:
            if complexity > 0:
                self.classes[class_name].complexity = complexity
            if mutation_score >= 0:
                self.classes[class_name].mutation_score = mutation_score
        else:
            self.classes[class_name] = JavaClass(class_name, complexity, mutation_score)
            
    def cleanup_incomplete_classes(self):
        """Remove classes that are not in both reports"""
        to_remove = []
        for class_name, java_class in self.classes.items():
            print(f"Class: {class_name}, Complexity: {java_class.complexity}, Mutation Score: {java_class.mutation_score}")
            if java_class.complexity == 0 or java_class.mutation_score <0: # if they are the default values assigned in "add_class"
                to_remove.append(class_name)
        
        for class_name in to_remove:
            self.classes.pop(class_name)

class Project:
    def __init__(self, name: str):
        self.name = name # Name of project
        self.packages = {} # Dictionary of {package_name : Package}
    
    def add_package(self, package_name: str):
        if package_name not in self.packages:
            self.packages[package_name] = Package(package_name)
        return self.packages[package_name]
    
    def cleanup_incomplete_classes(self):
        """Clean up all packages to remove incomplete classes"""
        for package in self.packages.values():
            package.cleanup_incomplete_classes()
        
        empty_packages = []
        for package_name, package in self.packages.items():
            if not package.classes:
                empty_packages.append(package_name)
        
        for package_name in empty_packages:
            self.packages.pop(package_name)


