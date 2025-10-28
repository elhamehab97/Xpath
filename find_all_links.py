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

def find_all_links_and_forms(file_path):
    """Find all links and forms in the file"""
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
            print(f"\nForm {i+1}:")
            print(f"  ID: {form.get('id', 'No ID')}")
            print(f"  Class: {form.get('class', 'No class')}")
            print(f"  XPath: {get_xpath(form)}")
            
            # Find all divs within this form
            divs = form.xpath(".//div")
            print(f"  Contains {len(divs)} divs")
            
            # Find all links within this form
            links = form.xpath(".//a")
            print(f"  Contains {len(links)} links")
            
            for j, link in enumerate(links):
                print(f"    Link {j+1}: {link.text_content().strip()[:50]}...")
                print(f"      href: {link.get('href', 'No href')}")
                print(f"      XPath: {get_xpath(link)}")
        
        # Find all links in the document
        all_links = doc.xpath("//a")
        print(f"\nFound {len(all_links)} total links in document")
        
        # Show first 10 links
        for i, link in enumerate(all_links[:10]):
            print(f"  Link {i+1}: {link.text_content().strip()[:50]}...")
            print(f"    href: {link.get('href', 'No href')}")
            print(f"    XPath: {get_xpath(link)}")
        
        return doc
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def try_original_xpath(doc, xpath):
    """Try to find element using the original XPath"""
    try:
        elements = doc.xpath(xpath)
        if elements:
            element = elements[0]
            print(f"Found element with original XPath:")
            print(f"  Tag: {element.tag}")
            print(f"  Text: {element.text_content().strip()}")
            print(f"  Attributes: {element.attrib}")
            return element
        else:
            print(f"No element found with XPath: {xpath}")
            return None
    except Exception as e:
        print(f"Error with XPath {xpath}: {e}")
        return None

if __name__ == "__main__":
    old_file = "/workspace/Microsoft_old.html"
    new_file = "/workspace/Microsoft_new.html"
    original_xpath = "/html[1]/body[1]/div[1]/form[1]/div[2]/div[1]/div[1]/a[1]"
    
    print("=== Analyzing Old File ===")
    old_doc = find_all_links_and_forms(old_file)
    
    print("\n=== Trying Original XPath on Old File ===")
    old_element = try_original_xpath(old_doc, original_xpath)
    
    print("\n=== Analyzing New File ===")
    new_doc = find_all_links_and_forms(new_file)
    
    print("\n=== Trying Original XPath on New File ===")
    new_element = try_original_xpath(new_doc, original_xpath)
    
    if old_element and new_element:
        print(f"\nBoth files have elements matching the original XPath")
        print(f"Old element: {old_element.text_content().strip()}")
        print(f"New element: {new_element.text_content().strip()}")
        print(f"Final result: {original_xpath}")
    elif old_element:
        print(f"\nOnly old file has element matching the original XPath")
        print(f"Final result: null")
    else:
        print(f"\nNeither file has element matching the original XPath")
        print(f"Final result: null")