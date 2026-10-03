import re
import os

html_file = r'E:\pfppee\index.html'
projects_file = r'E:\pfppee\projects.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new gallery content for index.html (4 videos)
videos_index = [
    "Bizkit-4.mp4", "tradex-motion.mp4",
    "Malanchi-1.mp4", "0527.mp4" # using 0527.mp4 instead of 0525.mp4
]

cols_index = [[videos_index[0], videos_index[1]], [videos_index[2], videos_index[3]]]

def generate_item(video_name, aspect="aspect-[9/12]"):
    title = video_name.split('-')[0].split('.')[0].upper()
    return f'''<div class="gallery-item group cursor-pointer {aspect} w-full relative bg-midnight-light overflow-hidden">
    <video loop muted playsinline class="cinematic-video w-full h-full object-cover opacity-80 group-hover:opacity-100 grayscale group-hover:grayscale-0 transition-all duration-700">
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

gallery_html_index = '<div class="cinematic-gallery grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-12 w-full max-w-4xl mx-auto">\n'
for i, col in enumerate(cols_index):
    mt = "mt-0"
    if i == 1: mt = "mt-12 md:mt-24"
    
    gallery_html_index += f'    <div class="gallery-column flex flex-col gap-12 {mt}">\n'
    for v in col:
        gallery_html_index += "        " + generate_item(v).replace("\n", "\n        ") + "\n"
    gallery_html_index += '    </div>\n'
gallery_html_index += '</div>'

# Replace in index.html
pattern = re.compile(r'<div\s+class="cinematic-gallery[^>]*>.*?</div>(?=\s*<div\s+class="mt-16 text-center">)', re.DOTALL)
new_html = pattern.sub(gallery_html_index.replace('\\', '\\\\'), html, count=1)

# Update the "View All Projects" link in index.html
new_html = new_html.replace('<button\n                            class="inline-flex items-center', '<a href="projects.html"\n                            class="inline-flex items-center')
new_html = new_html.replace('</button>\n                    </div>\n                </div>\n            </section>', '</a>\n                    </div>\n                </div>\n            </section>')


with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)


# Now create projects.html
# Let's read the list of all videos in E:\pfppee\assets\works
works_dir = r'E:\pfppee\assets\works'
all_videos = [f for f in os.listdir(works_dir) if f.endswith('.mp4')]

# we will make a full grid of these videos
cols_proj = [[], [], []]
for i, v in enumerate(all_videos):
    cols_proj[i % 3].append(v)

def generate_proj_item(video_name):
    title = video_name.split('-')[0].split('.')[0].upper()
    return f'''<div class="gallery-item group cursor-pointer aspect-video w-full relative bg-midnight-light overflow-hidden rounded-xl">
    <video loop muted playsinline class="cinematic-video w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-all duration-700">
        <source src="./assets/works/{video_name}" type="video/mp4">
    </video>
    <div class="absolute inset-0 bg-gradient-to-t from-midnight via-transparent to-transparent opacity-80 pointer-events-none"></div>
    
    <!-- Controls overlay -->
    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-20">
        <button class="play-btn w-12 h-12 mx-2 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/40 hover:bg-white/40 transition-colors">
            <span class="material-symbols-outlined text-white">play_arrow</span>
        </button>
        <button class="pause-btn w-12 h-12 mx-2 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/40 hover:bg-white/40 transition-colors hidden">
            <span class="material-symbols-outlined text-white">pause</span>
        </button>
        <button class="skip-btn w-12 h-12 mx-2 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/40 hover:bg-white/40 transition-colors">
            <span class="material-symbols-outlined text-white">skip_next</span>
        </button>
    </div>

    <div class="gallery-overlay absolute bottom-0 left-0 w-full p-6 border-t border-white/10 z-10">
        <div class="flex justify-between items-end">
            <div>
                <h3 class="text-2xl font-serif font-bold text-white mb-1">{title}</h3>
                <p class="text-xs font-sans italic text-slate-300 font-light line-clamp-2">A creative digital project showcasing motion design and editing skills.</p>
            </div>
        </div>
    </div>
</div>'''

gallery_html_proj = '<div class="cinematic-gallery grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full mt-10">\n'
for v in all_videos:
    gallery_html_proj += generate_proj_item(v) + '\n'
gallery_html_proj += '</div>'

# We'll use index.html as a base but remove sections we don't need for projects.html
proj_html = html

# Replace gallery title
proj_html = proj_html.replace('Cinematic Gallery', 'All Projects')
proj_html = proj_html.replace('Selected Works', 'Complete Portfolio')

# Replace the gallery content
proj_html = pattern.sub(gallery_html_proj.replace('\\', '\\\\'), proj_html, count=1)

# Remove the "View All Projects" button section
proj_html = re.sub(r'<div class="mt-16 text-center">.*?</div>\n\s*</div>\n\s*</section>', r'</div>\n            </section>', proj_html, flags=re.DOTALL)

# Add specific script for custom controls
controls_js = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const galleryItems = document.querySelectorAll('.gallery-item');
            galleryItems.forEach(item => {
                const video = item.querySelector('.cinematic-video');
                const playBtn = item.querySelector('.play-btn');
                const pauseBtn = item.querySelector('.pause-btn');
                const skipBtn = item.querySelector('.skip-btn');
                
                if (video) {
                    if (playBtn && pauseBtn) {
                        playBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            video.play();
                            playBtn.classList.add('hidden');
                            pauseBtn.classList.remove('hidden');
                        });
                        
                        pauseBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            video.pause();
                            pauseBtn.classList.add('hidden');
                            playBtn.classList.remove('hidden');
                        });
                        
                        video.addEventListener('ended', () => {
                            pauseBtn.classList.add('hidden');
                            playBtn.classList.remove('hidden');
                        });
                    }
                    
                    if(skipBtn) {
                        skipBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            video.currentTime += 5; // Skip 5 seconds
                        });
                    }
                    
                    // Simple hover play is disabled on projects.html since we have controls
                    // If we still want hover play:
                    // item.addEventListener('mouseenter', () => video.play());
                    // item.addEventListener('mouseleave', () => video.pause());
                }
            });
        });
    </script>
"""

# replace the old hover script with the new controls script
proj_html = re.sub(r'<script>\n\s*document.addEventListener\(\'DOMContentLoaded\'.*?</script>', controls_js, proj_html, flags=re.DOTALL)


with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(proj_html)

print("Updated index.html and created projects.html")
