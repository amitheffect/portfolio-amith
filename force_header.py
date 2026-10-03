from bs4 import BeautifulSoup
import os

files_to_fix = [r'E:\pfppee\index.html', r'E:\pfppee\projects.html']

for file_path in files_to_fix:
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    header = soup.find('header')
    body = soup.find('body')
    
    if header and body:
        # Move the header to be the absolute first child of body to escape any container bugs
        header.extract()
        body.insert(0, header)
        
        # Clean up header classes to guarantee it stays fixed and highly visible
        classes = header.get('class', [])
        # Remove any z-index or bg classes that might conflict
        classes = [c for c in classes if not (c.startswith('z-') or c.startswith('bg-'))]
        
        # Add rock-solid fixed header classes
        classes.extend(['fixed', 'top-0', 'left-0', 'w-full', 'z-[100]', 'bg-midnight/90', 'backdrop-blur-xl', 'border-b', 'border-white/10', 'shadow-2xl'])
        
        header['class'] = classes
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Header forcibly moved to body root and fixed with z-[100].")
