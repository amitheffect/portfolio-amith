import os
import re

html_file = r'E:\pfppee\index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new gallery content
videos = [
    "Apis-1.mp4", "Apis-2.mp4", "Apis-3.mp4", "Apis-4.mp4",
    "Bizkit-1.mp4", "Bizkit-2.mp4", "Bizkit-3.mp4", "Bizkit-4.mp4",
    "Malanchi-1.mp4", "Malanchi-2.mp4", "Malanchi-3.mp4",
    "Zainex-1.mp4", "tradex-motion.mp4", "tradexsyndicate.mp4"
]

cols = [[], [], []]
for i, v in enumerate(videos):
    cols[i % 3].append(v)

def generate_item(video_name):
    # Give a default title based on filename
    title = video_name.split('-')[0].split('.')[0].upper()
    return f'''<div class="gallery-item group cursor-pointer aspect-[9/12] w-full relative bg-midnight-light overflow-hidden">
    <video autoplay loop muted playsinline class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700">
        <source src="./assets/works/{video_name}" type="video/mp4">
    </video>
    <div class="absolute inset-0 bg-gradient-to-t from-midnight via-transparent to-transparent opacity-60 pointer-events-none"></div>
    <div class="gallery-overlay absolute bottom-0 left-0 w-full p-8 border-t border-white/10">
        <div class="flex justify-between items-end">
            <div>
                <h3 class="text-3xl font-serif font-bold text-white mb-1">{title}</h3>
                <p class="text-sm font-sans italic text-blue-200 tracking-wide font-light">Project • Video</p>
            </div>
            <div class="w-12 h-12 rounded-full border border-white/30 flex items-center justify-center bg-white/10 backdrop-blur-sm group-hover:bg-white group-hover:text-midnight transition-colors">
                <span class="material-symbols-outlined text-lg">arrow_outward</span>
            </div>
        </div>
    </div>
</div>'''

gallery_html = '<div class="cinematic-gallery grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-12 w-full">\n'
for i, col in enumerate(cols):
    mt = "mt-0"
    if i == 1: mt = "mt-12 md:mt-24"
    if i == 2: mt = "mt-0 md:mt-48 hidden lg:flex"
    
    gallery_html += f'    <div class="gallery-column flex flex-col gap-12 {mt}">\n'
    for v in col:
        gallery_html += "        " + generate_item(v).replace("\n", "\n        ") + "\n"
    gallery_html += '    </div>\n'
gallery_html += '</div>'

# Regex to find the existing cinematic-gallery div and replace it
# We need to match <div class="cinematic-gallery grid ... w-full"> to its closing </div> which is right before <div class="mt-16 text-center">
pattern = re.compile(r'<div\s+class="cinematic-gallery[^>]*>.*?</div>(?=\s*<div\s+class="mt-16 text-center">)', re.DOTALL)

if pattern.search(html):
    html = pattern.sub(gallery_html.replace('\\', '\\\\'), html, count=1)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Gallery successfully replaced.")
else:
    print("Failed to find gallery section using regex.")
