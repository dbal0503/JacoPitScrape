import re
from bs4 import BeautifulSoup

def find_complexity_column(table):
    """Find the index of the complexity column in a JaCoCo table"""
    headers = table.find('thead').find_all('td')
    for i, header in enumerate(headers):
        if 'Complexity' in header.text or 'Cxty' in header.text:
            return i
    return None

def extract_number(text):
    """Extract first number from text, handling percentages"""
    matches = re.findall(r'(\d+)%?', text)
    if matches:
        return int(matches[0])
    return None

def extract_class_complexity(html_content):
    # Extract complexity metrics from JaCoCo HTML content
    # BeautifulSoup is used to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    
    table = soup.find('table', id='coveragetable')
    # If the table is not found, return an empty dictionary
    if not table:
        return result
    
    complexity_col = find_complexity_column(table)
    # If the complexity column is not found, return an empty dictionary
    if complexity_col is None:
        return result
    
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        # If the number of cells is greater than the complexity column, extract the class name
        if len(cells) > complexity_col:
            class_name = cells[0].text.strip()
            # If the class name is "Total", skip the row
            if class_name.startswith("org.") or class_name.startswith("com."):
                continue
            if class_name == "Total":
                continue
            # If the class name ends with ".java", remove the ".java" extension
            if class_name.endswith(".java"):
                class_name = class_name[:-5]
            # Extract the complexity text from the cell
            complexity_text = cells[complexity_col].text.strip()
            # Extract the number from the complexity text
            complexity = extract_number(complexity_text) or 0
            # If the complexity is greater than 0, add the class name and complexity to the result
            if complexity > 0:
                result[class_name] = complexity
    
    return result

def has_complexity_data(html_content):
    """Check if the HTML content has complexity data"""
    soup = BeautifulSoup(html_content, 'html.parser')
    complexity_header = soup.find('td', text=re.compile(r'Complexity|Cxty'))
    return complexity_header is not None
