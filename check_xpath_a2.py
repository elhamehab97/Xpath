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

def try_xpath(doc, xpath, file_name):
    """Try to find element using the given XPath"""
    try:
        elements = doc.xpath(xpath)
        if elements:
            element = elements[0]
            print(f"Found element in {file_name} with XPath: {xpath}")
            print(f"  Tag: {element.tag}")
            print(f"  Text: '{element.text_content().strip()}'")
            print(f"  Attributes: {element.attrib}")
            return element
        else:
            print(f"No element found in {file_name} with XPath: {xpath}")
            return None
    except Exception as e:
        print(f"Error with XPath {xpath} in {file_name}: {e}")
        return None

def find_matching_element(old_doc, new_doc, old_element):
    """Find matching element in new document based on old element characteristics"""
    if not old_element:
        return None
    
    print(f"\nLooking for matching element in new file...")
    print(f"Old element characteristics:")
    print(f"  Tag: {old_element.tag}")
    print(f"  Text: '{old_element.text_content().strip()}'")
    print(f"  Attributes: {old_element.attrib}")
    
    # Get characteristics of the old element
    old_tag = old_element.tag
    old_text = old_element.text_content().strip()
    old_attrs = old_element.attrib
    
    # Look for similar elements in new document
    # Try to find elements with same tag and similar text or attributes
    similar_elements = []
    
    # Find all elements with same tag
    all_elements = new_doc.xpath(f"//{old_tag}")
    
    for elem in all_elements:
        elem_text = elem.text_content().strip()
        elem_attrs = elem.attrib
        
        # Check if text is similar or if it's a link with similar href
        text_match = elem_text == old_text
        href_match = (old_tag == 'a' and 'href' in elem_attrs and 'href' in old_attrs and 
                     elem_attrs.get('href') == old_attrs.get('href'))
        class_match = ('class' in elem_attrs and 'class' in old_attrs and 
                      elem_attrs.get('class') == old_attrs.get('class'))
        
        if text_match or href_match or class_match:
            similar_elements.append(elem)
    
    if similar_elements:
        best_match = similar_elements[0]
        print(f"\nFound {len(similar_elements)} potential matches")
        print(f"Best match:")
        print(f"  Tag: {best_match.tag}")
        print(f"  Text: '{best_match.text_content().strip()}'")
        print(f"  Attributes: {best_match.attrib}")
        
        # Generate XPath for the best match
        xpath = get_xpath(best_match)
        print(f"\nGenerated XPath: {xpath}")
        return xpath
    else:
        print("No matching element found")
        return None

if __name__ == "__main__":
    old_file = "/workspace/Microsoft_old.html"
    new_file = "/workspace/Microsoft_new.html"
    old_xpath = "/html[1]/body[1]/div[1]/form[1]/div[2]/div[1]/div[1]/a[2]"
    
    # Parse both files
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_content = f.read()
        old_doc = html.fromstring(old_content)
        
        with open(new_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        new_doc = html.fromstring(new_content)
        
        # Try to find element in old file
        old_element = try_xpath(old_doc, old_xpath, "old file")
        
        if old_element:
            # Find matching element in new file
            result = find_matching_element(old_doc, new_doc, old_element)
            if result:
                print(f"\nFinal result: {result}")
            else:
                print(f"\nFinal result: null")
        else:
            print(f"\nFinal result: null")
            
    except Exception as e:
        print(f"Error: {e}")
        print(f"\nFinal result: null")