import re
from bs4 import BeautifulSoup

def find_mutation_column(table):
    """Find the index of the mutation coverage column in a PIT table"""
    headers = table.find('thead').find_all('th')
    for i, header in enumerate(headers):
        if 'Mutation Coverage' in header.text:
            return i
    return 2  

def extract_number(text):
    """Extract first number from text, handling percentages"""
    matches = re.findall(r'(\d+)%?', text)
    if matches:
        return int(matches[0])
    return None

def extract_mutation_scores(html_content):
    """Extract mutation score metrics from PIT HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}
    
    class_table = None
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        if 'Breakdown by Class' in heading.text:
            class_table = heading.find_next('table')
            break
    
    if not class_table:
        return result
    
    mutation_col = find_mutation_column(class_table)
    
    for row in class_table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        
        if len(cells) > mutation_col:
            class_cell = cells[0]
            class_link = class_cell.find('a')
            
            if class_link:
                class_name = class_link.text.strip()
            else:
                class_name = class_cell.text.strip()
            
            if class_name.startswith("org.") or class_name.startswith("com."):
                continue
            
            if class_name.endswith(".java"):
                class_name = class_name[:-5]
            
            mutation_div = cells[mutation_col].find('div', class_='coverage_percentage')
            if mutation_div:
                mutation_text = mutation_div.text.strip()
                mutation_score = extract_number(mutation_text) or 0
                
                if mutation_score >= 0:
                    result[class_name] = mutation_score
    
    return result

def has_mutation_data(html_content):
    """Check if the HTML content has mutation data"""
    return "Mutation Coverage" in html_content and "Breakdown by Class" in html_content
