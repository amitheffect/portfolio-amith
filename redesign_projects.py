import re
import os

base_file = r'E:\pfppee\index.html'
projects_file = r'E:\pfppee\projects.html'

with open(base_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract head and header
head_match = re.search(r'(<!DOCTYPE html>.*?</header>)', html, re.DOTALL)
if head_match:
    head_html = head_match.group(1)
else:
    head_html = ""

# Get videos
works_dir = r'E:\pfppee\assets\works'
all_videos = [f for f in os.listdir(works_dir) if f.endswith('.mp4')]

# Generate Masonry items
items_html = ""
for v in all_videos:
    title = v.split('-')[0].split('.')[0].upper()
    items_html += f'''
    <div class="gallery-item group relative bg-midnight-light rounded-2xl overflow-hidden break-inside-avoid mb-6 shadow-2xl border border-white/5">
        <video loop muted playsinline class="cinematic-video w-full h-auto object-cover opacity-90 transition-opacity duration-700">
            <source src="./assets/works/{v}" type="video/mp4">
        </video>
        
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-midnight/90 via-midnight/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        
        <!-- Center Play Button (Large) -->
        <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-20 pointer-events-none">
            <button class="center-play-btn w-16 h-16 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center border border-white/20 text-white shadow-[0_0_30px_rgba(255,255,255,0.1)] pointer-events-auto hover:bg-white hover:text-midnight transition-all duration-300 transform hover:scale-110">
                <span class="material-symbols-outlined text-3xl ml-1">play_arrow</span>
            </button>
        </div>

        <!-- Bottom Controls & Info -->
        <div class="absolute bottom-0 left-0 w-full p-6 translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-500 z-30">
            <div class="flex justify-between items-end mb-4">
                <div>
                    <h3 class="text-2xl font-serif font-bold text-white mb-1 drop-shadow-md">{title}</h3>
                    <p class="text-xs font-sans text-blue-200 tracking-wide font-light">Motion / Video</p>
                </div>
                <div class="flex gap-2">
                    <button class="mute-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                        <span class="material-symbols-outlined text-sm">volume_off</span>
                    </button>
                    <button class="skip-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                        <span class="material-symbols-outlined text-sm">skip_next</span>
                    </button>
                </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full h-1 bg-white/20 rounded-full overflow-hidden cursor-pointer progress-container">
                <div class="progress-bar h-full bg-blue-400 w-0 pointer-events-none"></div>
            </div>
        </div>
    </div>
'''

new_page = head_html + f'''
    <main class="flex-grow w-full pt-32 pb-24">
        <div class="max-w-[1600px] mx-auto px-6 lg:px-12">
            <div class="mb-16 text-center space-y-4">
                <h1 class="font-serif italic text-5xl md:text-6xl text-white tracking-tight">Complete Portfolio</h1>
                <p class="text-slate-400 font-light">Explore all motion graphics, UI designs, and video edits.</p>
            </div>
            
            <!-- Masonry Grid -->
            <div class="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6">
                {items_html}
            </div>
        </div>
    </main>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const items = document.querySelectorAll('.gallery-item');
            
            items.forEach(item => {{
                const video = item.querySelector('.cinematic-video');
                const centerBtn = item.querySelector('.center-play-btn');
                const centerIcon = centerBtn.querySelector('span');
                const muteBtn = item.querySelector('.mute-btn');
                const muteIcon = muteBtn.querySelector('span');
                const skipBtn = item.querySelector('.skip-btn');
                const progressContainer = item.querySelector('.progress-container');
                const progressBar = item.querySelector('.progress-bar');
                
                let isPlaying = false;

                // Play/Pause toggle
                centerBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    if(video.paused) {{
                        video.play();
                        centerIcon.innerText = 'pause';
                    }} else {{
                        video.pause();
                        centerIcon.innerText = 'play_arrow';
                    }}
                }});

                // Update icon on actual video state change (in case of auto-pause etc)
                video.addEventListener('play', () => centerIcon.innerText = 'pause');
                video.addEventListener('pause', () => centerIcon.innerText = 'play_arrow');

                // Mute toggle
                muteBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    video.muted = !video.muted;
                    muteIcon.innerText = video.muted ? 'volume_off' : 'volume_up';
                }});

                // Skip 5 seconds
                skipBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    video.currentTime = Math.min(video.currentTime + 5, video.duration);
                }});

                // Update progress bar
                video.addEventListener('timeupdate', () => {{
                    if(video.duration) {{
                        const percent = (video.currentTime / video.duration) * 100;
                        progressBar.style.width = percent + '%';
                    }}
                }});

                // Seek on progress bar click
                progressContainer.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const rect = progressContainer.getBoundingClientRect();
                    const pos = (e.clientX - rect.left) / rect.width;
                    video.currentTime = pos * video.duration;
                }});
                
                // Optional: Auto-pause when hovering out to save resources
                item.addEventListener('mouseleave', () => {{
                    if(!video.paused) {{
                        video.pause();
                        centerIcon.innerText = 'play_arrow';
                    }}
                }});
            }});
        }});
    </script>
</body>
</html>
'''

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(new_page)

print("projects.html redesigned with masonry layout and advanced player controls.")
