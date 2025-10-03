#!/usr/bin/env python3
import re
from lxml import html, etree
import sys

def get_xpath(element):
    """Generate XPath for an element"""
    path = []
    while element is not None:
        tag = element.tag
        if tag is None:
            break
        
        # Get position among siblings with same tag
        siblings = element.getparent()
        if siblings is not None:
            same_tag_siblings = [s for s in siblings if s.tag == tag]
            if len(same_tag_siblings) > 1:
                position = same_tag_siblings.index(element) + 1
                path.insert(0, f"{tag}[{position}]")
            else:
                path.insert(0, tag)
        else:
            path.insert(0, tag)
        
        element = element.getparent()
    
    return "/" + "/".join(path)

def analyze_form_structure(form, form_index, file_name):
    """Analyze the structure of a form in detail"""
    print(f"\n=== Form {form_index} in {file_name} ===")
    print(f"Form XPath: {get_xpath(form)}")
    print(f"Form ID: {form.get('id', 'No ID')}")
    print(f"Form Class: {form.get('class', 'No class')}")
    
    # Find all divs within this form
    divs = form.xpath(".//div")
    print(f"Total divs in form: {len(divs)}")
    
    # Find all links within this form
    links = form.xpath(".//a")
    print(f"Total links in form: {len(links)}")
    
    # Analyze the div structure
    def analyze_div_structure(div, level=0, max_level=3):
        indent = "  " * level
        div_xpath = get_xpath(div)
        div_class = div.get('class', 'No class')
        div_id = div.get('id', 'No ID')
        
        print(f"{indent}Div at level {level}: {div_xpath}")
        print(f"{indent}  Class: {div_class}")
        print(f"{indent}  ID: {div_id}")
        
        # Find direct child divs
        child_divs = [child for child in div if child.tag == 'div']
        print(f"{indent}  Direct child divs: {len(child_divs)}")
        
        # Find direct child links
        child_links = [child for child in div if child.tag == 'a']
        print(f"{indent}  Direct child links: {len(child_links)}")
        
        for i, link in enumerate(child_links):
            link_xpath = get_xpath(link)
            link_text = link.text_content().strip()[:50]
            link_href = link.get('href', 'No href')
            print(f"{indent}    Link {i+1}: {link_text}...")
            print(f"{indent}      XPath: {link_xpath}")
            print(f"{indent}      href: {link_href}")
        
        # Recursively analyze child divs (up to max_level)
        if level < max_level:
            for child_div in child_divs:
                analyze_div_structure(child_div, level + 1, max_level)
    
    # Analyze the form's direct child divs
    direct_child_divs = [child for child in form if child.tag == 'div']
    print(f"Direct child divs of form: {len(direct_child_divs)}")
    
    for i, div in enumerate(direct_child_divs):
        print(f"\n--- Direct child div {i+1} ---")
        analyze_div_structure(div, 1, 3)

def find_forms_with_links(file_path):
    """Find all forms and analyze their structure"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse HTML
        doc = html.fromstring(content)
        
        print(f"Analyzing {file_path}...")
        
        # Find all forms
        forms = doc.xpath("//form")
        print(f"Found {len(forms)} forms")
        
        for i, form in enumerate(forms):
            analyze_form_structure(form, i+1, file_path)
        
        # Also look for any div structures that might match the expected pattern
        print(f"\n=== Looking for div[2]/div[1]/div[1]/a patterns ===")
        
        # Find all divs that have the structure: div[2]/div[1]/div[1]/a
        potential_matches = []
        
        # Look for divs that have at least 2 direct child divs
        all_divs = doc.xpath("//div")
        for div in all_divs:
            child_divs = [child for child in div if child.tag == 'div']
            if len(child_divs) >= 2:
                # Check if the second div has at least 1 child div
                second_div = child_divs[1] if len(child_divs) > 1 else None
                if second_div:
                    second_div_children = [child for child in second_div if child.tag == 'div']
                    if len(second_div_children) >= 1:
                        # Check if the first child of second div has at least 2 links
                        first_child = second_div_children[0]
                        child_links = [child for child in first_child if child.tag == 'a']
                        if len(child_links) >= 2:
                            potential_matches.append((div, second_div, first_child, child_links))
        
        print(f"Found {len(potential_matches)} potential matches for div[2]/div[1]/div[1]/a[2] pattern")
        
        for i, (parent_div, second_div, first_child, links) in enumerate(potential_matches):
            print(f"\nPotential match {i+1}:")
            print(f"  Parent div XPath: {get_xpath(parent_div)}")
            print(f"  Second div XPath: {get_xpath(second_div)}")
            print(f"  First child XPath: {get_xpath(first_child)}")
            print(f"  Links found: {len(links)}")
            
            for j, link in enumerate(links):
                link_xpath = get_xpath(link)
                link_text = link.text_content().strip()[:50]
                print(f"    Link {j+1}: {link_text}...")
                print(f"      XPath: {link_xpath}")
        
        return doc
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

if __name__ == "__main__":
    old_file = "/workspace/Microsoft_old.html"
    new_file = "/workspace/Microsoft_new.html"
    
    print("=== Analyzing Old File ===")
    old_doc = find_forms_with_links(old_file)
    
    print("\n" + "="*80)
    print("=== Analyzing New File ===")
    new_doc = find_forms_with_links(new_file)
    
    print(f"\nFinal result: null")