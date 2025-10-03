#!/usr/bin/env python3
import re
from lxml import html
import sys

def find_xpath_element(file_path, xpath):
    """Find element using XPath in HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse HTML
        doc = html.fromstring(content)
        
        # Find element using XPath
        elements = doc.xpath(xpath)
        
        if elements:
            element = elements[0]
            print(f"Found element in {file_path}:")
            print(f"Tag: {element.tag}")
            print(f"Text: {element.text_content().strip()}")
            print(f"Attributes: {element.attrib}")
            return element
        else:
            print(f"No element found with XPath: {xpath}")
            return None
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def find_matching_element(old_file, new_file, old_xpath):
    """Find matching element in new file based on old element"""
    # First find the element in old file
    old_element = find_xpath_element(old_file, old_xpath)
    if not old_element:
        return None
    
    print(f"\nLooking for matching element in {new_file}...")
    
    # Get characteristics of the old element
    old_tag = old_element.tag
    old_text = old_element.text_content().strip()
    old_attrs = old_element.attrib
    
    print(f"Old element characteristics:")
    print(f"  Tag: {old_tag}")
    print(f"  Text: '{old_text}'")
    print(f"  Attributes: {old_attrs}")
    
    # Parse new file
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        new_doc = html.fromstring(new_content)
        
        # Look for similar elements
        # Try to find elements with same tag and similar text
        similar_elements = []
        
        # Find all elements with same tag
        all_elements = new_doc.xpath(f"//{old_tag}")
        
        for elem in all_elements:
            elem_text = elem.text_content().strip()
            # Check if text is similar or if it's a link with similar href
            if (elem_text == old_text or 
                (old_tag == 'a' and 'href' in elem.attrib and 'href' in old_attrs and 
                 elem.attrib.get('href') == old_attrs.get('href'))):
                similar_elements.append(elem)
        
        if similar_elements:
            best_match = similar_elements[0]
            print(f"\nFound {len(similar_elements)} potential matches")
            print(f"Best match:")
            print(f"  Tag: {best_match.tag}")
            print(f"  Text: '{best_match.text_content().strip()}'")
            print(f"  Attributes: {best_match.attrib}")
            
            # Generate XPath for the best match
            xpath = new_doc.getpath(best_match)
            print(f"\nGenerated XPath: {xpath}")
            return xpath
        else:
            print("No matching element found")
            return None
            
    except Exception as e:
        print(f"Error processing {new_file}: {e}")
        return None

if __name__ == "__main__":
    old_file = "/workspace/Microsoft_old.html"
    new_file = "/workspace/Microsoft_new.html"
    old_xpath = "/html[1]/body[1]/div[1]/form[1]/div[2]/div[1]/div[1]/a[1]"
    
    result = find_matching_element(old_file, new_file, old_xpath)
    if result:
        print(f"\nFinal result: {result}")
    else:
        print("\nFinal result: null")