import re

html_file = r'E:\pfppee\index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the video tags
# From: <video autoplay loop muted playsinline class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700">
# To: <video loop muted playsinline class="cinematic-video w-full h-full object-cover opacity-80 group-hover:opacity-100 grayscale group-hover:grayscale-0 transition-all duration-700">

old_video_tag = '<video autoplay loop muted playsinline class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700">'
new_video_tag = '<video loop muted playsinline class="cinematic-video w-full h-full object-cover opacity-80 group-hover:opacity-100 grayscale group-hover:grayscale-0 transition-all duration-700">'

html = html.replace(old_video_tag, new_video_tag)

# Add the JavaScript at the end of the body
js_snippet = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const galleryItems = document.querySelectorAll('.gallery-item');
            galleryItems.forEach(item => {
                const video = item.querySelector('.cinematic-video');
                if (video) {
                    item.addEventListener('mouseenter', () => {
                        video.play();
                    });
                    item.addEventListener('mouseleave', () => {
                        video.pause();
                    });
                }
            });
        });
    </script>
"""

# Check if script is already added, if not, add it before </body>
if 'const galleryItems = document.querySelectorAll(' not in html:
    html = html.replace('</body>', js_snippet + '</body>')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Hover logic and grayscale applied.")
