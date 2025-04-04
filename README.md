# SOEN 345 Cyclomatic Complexity vs Mutation Score

This project analyses Java project metrics from JaCoCo and PIT reports to extract cyclomatic complexity and mutation scores and compare them at the class level.

## Output



## Installation

1. Clone the repository
2. Install dependencies through requirements.txt:

```bash
pip install -r requirements.txt
```

```bash
python main.py /path/to/reports/directory
```

To export results to a CSV file:

```bash
python main.py /path/to/reports/directory --csv output.csv
```

To generate graphs and visualizations:

```bash
python main.py /path/to/reports/directory --graphs
```

To generate graphs as well as output csv:

```bash
python main.py /path/to/reports/directory --csv output.csv --graphs
```

## Project Structure
- `artifacts/`: UML Class Diagram describing data model 
- `models/`: Implementation of data model
- `utils/`: Utility modules for processing and displaying reports
    - `complexity.py`: Methods for extracting complexity data from JaCoCo reports
    - `mutation.py`: Methods for extracting mutation data from PIT reports
    - `report_processor.py`: Logic for finding and processing reports
    - `report_display.py`: Functions for displaying results
    - `visualization.py`: Functions for generating graphs and visualizations

## Expected Data Input Structure
This project expects the following data structure which is stardard for 
- `root/`
    - `jacoco/`
        - `Project1/`
            - `index.html`
            - `org.Package1`
                - `index.html`
                - `Class1`
                - `Class2`
                ...
            - `org.Package2`
            ...
        - `Project2/`
        - `Project3/`
        ...
    - `pit`
        - `Project1/`
            - `index.html`
            - `org.Package1`
                - `index.html`
                - `Class1`
                - `Class2`
                ...
            - `org.Package2`
            ...
        - `Project2/`
        - `Project3/`
        ...
        



## Output
Three graphs are generated:
- A table sorted in order with the classes with the greatest complexities 
- A histogram displaying the seperation in cyclomatic complexity and mutation score amongst the dataset
- A scatter plot of mutation score vs cylomatic complexity


The following is outputed to the console
- Project name:
- Package name:
- Class name with complexity and mutation score

It also provides summary statistics on the analyzed classes.

## Example Data
Example data is included in data/Projects which contains jacoco and PIT reports from severall defects4j projects.