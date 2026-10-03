from bs4 import BeautifulSoup
import os

index_file = r'E:\pfppee\index.html'
projects_file = r'E:\pfppee\projects.html'

def fix_html(file_path, is_projects=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Remove all data-aos attributes and unwrap empty divs
    for tag in soup.find_all(attrs={"data-aos": True}):
        del tag["data-aos"]
        # If it's a div and has no other attributes (no class, id, etc), unwrap it
        if tag.name == 'div' and not tag.attrs:
            tag.unwrap()

    # Make the header sticky and visible
    header = soup.find('header')
    if header:
        classes = header.get('class', [])
        # Ensure it has bg and blur classes
        new_classes = ['bg-midnight/80', 'backdrop-blur-lg', 'border-b', 'border-white/5']
        for c in new_classes:
            if c not in classes:
                classes.append(c)
        header['class'] = classes
        
        # Add 'Back to home' link logic for projects.html
        if is_projects:
            logo_link = header.find('a')
            if logo_link:
                logo_link['href'] = 'index.html'
                # Optionally append text to make it obvious
                # title = logo_link.find('h2')
                # if title: title.string = "oneunix.ae (Home)"

    # Add smooth animation CSS to the <head>
    head = soup.find('head')
    if head:
        anim_style = soup.new_tag('style')
        anim_style.string = """
            .animate-on-load {
                animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                opacity: 0;
                transform: translateY(30px);
            }
            .delay-100 { animation-delay: 100ms; }
            .delay-200 { animation-delay: 200ms; }
            .delay-300 { animation-delay: 300ms; }
            
            @keyframes fadeInUp {
                to { opacity: 1; transform: translateY(0); }
            }
        """
        # Append only if not already there
        if "animate-on-load" not in str(head):
            head.append(anim_style)

    # Apply animate-on-load to main sections
    main = soup.find('main') or soup.find('body')
    sections = main.find_all('section', recursive=False)
    if not sections:
        # For projects.html which has div inside main
        sections = main.find_all('div', recursive=False)
        
    for i, section in enumerate(sections):
        sec_classes = section.get('class', [])
        if 'animate-on-load' not in sec_classes:
            sec_classes.append('animate-on-load')
            if i == 1: sec_classes.append('delay-100')
            if i == 2: sec_classes.append('delay-200')
            section['class'] = sec_classes

    # Save
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

fix_html(index_file, is_projects=False)
fix_html(projects_file, is_projects=True)
print("Applied fixes and animations.")
