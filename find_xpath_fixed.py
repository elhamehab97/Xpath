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

def analyze_html_structure(file_path):
    """Analyze HTML structure to understand the layout"""
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
        
        # Look for search-related forms specifically
        search_forms = doc.xpath("//form[contains(@class, 'search') or contains(@id, 'search')]")
        print(f"\nFound {len(search_forms)} search-related forms")
        
        for i, form in enumerate(search_forms):
            print(f"\nSearch Form {i+1}:")
            print(f"  ID: {form.get('id', 'No ID')}")
            print(f"  Class: {form.get('class', 'No class')}")
            
            # Get the XPath to this form
            form_xpath = get_xpath(form)
            print(f"  XPath: {form_xpath}")
            
            # Find all links within this form
            links = form.xpath(".//a")
            print(f"  Contains {len(links)} links")
            
            for j, link in enumerate(links):
                link_xpath = get_xpath(link)
                print(f"    Link {j+1}: {link.text_content().strip()[:50]}...")
                print(f"      XPath: {link_xpath}")
                print(f"      href: {link.get('href', 'No href')}")
        
        return doc
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def find_similar_elements(old_doc, new_doc):
    """Find similar elements between old and new documents"""
    print("\nLooking for similar elements...")
    
    # Find all forms in both documents
    old_forms = old_doc.xpath("//form")
    new_forms = new_doc.xpath("//form")
    
    print(f"Old document has {len(old_forms)} forms")
    print(f"New document has {len(new_forms)} forms")
    
    # Look for search forms specifically
    old_search_forms = old_doc.xpath("//form[contains(@class, 'search') or contains(@id, 'search')]")
    new_search_forms = new_doc.xpath("//form[contains(@class, 'search') or contains(@id, 'search')]")
    
    print(f"Old document has {len(old_search_forms)} search forms")
    print(f"New document has {len(new_search_forms)} search forms")
    
    if old_search_forms and new_search_forms:
        old_form = old_search_forms[0]
        new_form = new_search_forms[0]
        
        print(f"\nOld search form XPath: {get_xpath(old_form)}")
        print(f"New search form XPath: {get_xpath(new_form)}")
        
        # Find links in both forms
        old_links = old_form.xpath(".//a")
        new_links = new_form.xpath(".//a")
        
        print(f"Old search form has {len(old_links)} links")
        print(f"New search form has {len(new_links)} links")
        
        if old_links and new_links:
            old_link = old_links[0]
            new_link = new_links[0]
            
            print(f"\nOld first link:")
            print(f"  Text: '{old_link.text_content().strip()}'")
            print(f"  href: {old_link.get('href', 'No href')}")
            print(f"  XPath: {get_xpath(old_link)}")
            
            print(f"\nNew first link:")
            print(f"  Text: '{new_link.text_content().strip()}'")
            print(f"  href: {new_link.get('href', 'No href')}")
            print(f"  XPath: {get_xpath(new_link)}")
            
            return get_xpath(new_link)
    
    return None

if __name__ == "__main__":
    old_file = "/workspace/Microsoft_old.html"
    new_file = "/workspace/Microsoft_new.html"
    
    print("=== Analyzing Old File ===")
    old_doc = analyze_html_structure(old_file)
    
    print("\n=== Analyzing New File ===")
    new_doc = analyze_html_structure(new_file)
    
    if old_doc and new_doc:
        result = find_similar_elements(old_doc, new_doc)
        if result:
            print(f"\nFinal result: {result}")
        else:
            print("\nFinal result: null")
    else:
        print("\nFinal result: null")