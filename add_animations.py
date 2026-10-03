import re
import os

files_to_update = [r'E:\pfppee\index.html', r'E:\pfppee\projects.html']

aos_css = '    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">\n'
page_transition_css = """
    <style>
        /* Page Load Animation */
        body {
            animation: fadeInPage 0.8s ease-out forwards;
            opacity: 0;
        }
        @keyframes fadeInPage {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
"""

aos_js = """
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            AOS.init({
                duration: 800,
                once: true,
                offset: 100,
                easing: 'ease-out-cubic'
            });
        });
    </script>
"""

for filepath in files_to_update:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Add AOS CSS and Page Transition CSS
        if 'aos.css' not in html:
            html = html.replace('</head>', aos_css + page_transition_css + '</head>')
            
        # Add AOS JS
        if 'aos.js' not in html:
            html = html.replace('</body>', aos_js + '</body>')
            
        # Add data-aos attributes to sections/items
        # For index.html sections
        html = re.sub(r'(<section[^>]*class="[^"]*max-w-\[1200px\][^"]*"[^>]*>)', r'\1\n<div data-aos="fade-up">', html)
        # Note: we have to be careful not to break HTML. Actually, let's just add data-aos to the inner glass panels or specific divs.
        html = html.replace('class="glass-panel p-8 lg:p-16', 'data-aos="fade-up" class="glass-panel p-8 lg:p-16')
        html = html.replace('class="flex flex-col gap-16 items-center text-center"', 'data-aos="fade-up" class="flex flex-col gap-16 items-center text-center"')
        
        # For gallery items in both files
        html = html.replace('class="gallery-item', 'data-aos="fade-up" class="gallery-item')
        
        # Form integration for index.html
        if 'index.html' in filepath:
            html = html.replace('<form class="space-y-6">', 
                                '<form action="https://api.web3forms.com/submit" method="POST" class="space-y-6">\n' +
                                '                                <input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">\n' + 
                                '                                <input type="hidden" name="redirect" value="https://web3forms.com/success">\n')
            # Add name attributes to inputs so the form works
            html = html.replace('id="name" placeholder="John Doe" type="text" />', 'id="name" name="name" placeholder="John Doe" type="text" required />')
            html = html.replace('id="email" placeholder="john@company.com" type="email" />', 'id="email" name="email" placeholder="john@company.com" type="email" required />')
            html = html.replace('id="type">', 'id="type" name="project_type">')
            html = html.replace('id="budget">', 'id="budget" name="budget">')
            html = html.replace('id="message"', 'id="message" name="message" required')
            html = html.replace('<button\n                                    class="w-full h-14 rounded-full', '<button type="submit"\n                                    class="w-full h-14 rounded-full')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
        print(f"Updated {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Failed to update {filepath}: {e}")
