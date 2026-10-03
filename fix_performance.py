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

# Add a style block for high performance CSS rules
performance_css = """
    <style>
        /* Force hardware acceleration on videos */
        .cinematic-video {
            transform: translateZ(0);
            will-change: transform, opacity;
        }
        
        /* UI Layer visibility driven by pure CSS hover for max performance */
        .ui-layer {
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            pointer-events: none; /* Let clicks pass to buttons inside */
        }
        
        /* Show UI only on hover */
        .gallery-item:hover .ui-layer {
            opacity: 1;
        }
        
        /* Make buttons clickable inside the UI layer */
        .ui-layer button, .ui-layer .progress-container {
            pointer-events: auto;
        }

        /* Handle the grayscale focus mode purely via CSS */
        body.video-active .gallery-item {
            filter: grayscale(100%);
            opacity: 0.4;
            transition: all 0.5s ease;
        }
        
        body.video-active .gallery-item.is-playing {
            filter: grayscale(0%);
            opacity: 1;
            z-index: 50;
        }
    </style>
"""
head_html = head_html.replace('</head>', performance_css + '\n</head>')


works_dir = r'E:\pfppee\assets\works'
all_videos = [f for f in os.listdir(works_dir) if f.endswith('.mp4')]

items_html = ""
for v in all_videos:
    title = v.split('-')[0].split('.')[0].upper()
    items_html += f'''
    <div class="gallery-item relative bg-midnight-light rounded-2xl overflow-hidden break-inside-avoid mb-6 shadow-2xl border border-white/5 transition-all duration-500">
        <!-- Added preload="metadata" to stop browser from freezing by downloading 17 videos at once -->
        <video preload="metadata" loop playsinline class="cinematic-video w-full h-auto object-cover opacity-90 cursor-pointer">
            <source src="./assets/works/{v}" type="video/mp4">
        </video>
        
        <!-- UI LAYER (Controlled by CSS hover) -->
        <div class="ui-layer absolute inset-0 z-20 flex flex-col justify-between">
            
            <!-- Top Gradient (Just for looks) -->
            <div class="absolute inset-0 bg-gradient-to-t from-midnight/90 via-midnight/20 to-transparent pointer-events-none"></div>

            <!-- Center Play Button -->
            <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                <button class="center-play-btn w-16 h-16 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center border border-white/20 text-white shadow-[0_0_30px_rgba(255,255,255,0.1)] hover:bg-white hover:text-midnight transition-all duration-300 transform hover:scale-110">
                    <span class="material-symbols-outlined text-3xl ml-1">play_arrow</span>
                </button>
            </div>

            <!-- Bottom Controls -->
            <div class="absolute bottom-0 left-0 w-full p-6">
                <div class="flex justify-between items-end mb-4 relative z-30">
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
                        <button class="fullscreen-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                            <span class="material-symbols-outlined text-sm">fullscreen</span>
                        </button>
                    </div>
                </div>
                
                <!-- Progress Bar -->
                <div class="w-full h-1 bg-white/20 rounded-full overflow-hidden cursor-pointer progress-container relative z-30">
                    <div class="progress-bar h-full bg-blue-400 w-0 pointer-events-none"></div>
                </div>
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
            
            // Intersection Observer to only load videos when they scroll into view (Major Performance Boost)
            const videoObserver = new IntersectionObserver((entries, observer) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        const video = entry.target;
                        // Actually loading the video is handled by the browser if preload="metadata", 
                        // but we can ensure it's ready here.
                    }} else {{
                        // Pause if it scrolls out of view
                        const video = entry.target;
                        if (!video.paused) {{
                            video.pause();
                        }}
                    }}
                }});
            }}, {{ rootMargin: '200px' }});

            items.forEach(item => {{
                const video = item.querySelector('.cinematic-video');
                const centerBtn = item.querySelector('.center-play-btn');
                const centerIcon = centerBtn.querySelector('span');
                const muteBtn = item.querySelector('.mute-btn');
                const muteIcon = muteBtn.querySelector('span');
                const skipBtn = item.querySelector('.skip-btn');
                const fullscreenBtn = item.querySelector('.fullscreen-btn');
                const progressContainer = item.querySelector('.progress-container');
                const progressBar = item.querySelector('.progress-bar');
                
                // Unmute all videos initially but keep them paused
                // video.muted = false; // Actually, browsers block unmuted autoplay, so we leave it muted by default.
                
                videoObserver.observe(video);

                const togglePlay = (e) => {{
                    if(e) e.stopPropagation();
                    if(video.paused) {{
                        // Pause any other playing videos first (optional, but good UX)
                        document.querySelectorAll('video').forEach(v => {{
                            if(v !== video && !v.paused) v.pause();
                        }});
                        
                        // Play this video
                        const playPromise = video.play();
                        if (playPromise !== undefined) {{
                            playPromise.catch(error => {{
                                console.log("Playback prevented:", error);
                            }});
                        }}
                    }} else {{
                        video.pause();
                    }}
                }};

                // Click video itself to play/pause
                video.addEventListener('click', togglePlay);
                centerBtn.addEventListener('click', togglePlay);

                // When video plays
                video.addEventListener('play', () => {{
                    centerIcon.innerText = 'pause';
                    item.classList.add('is-playing');
                    document.body.classList.add('video-active');
                }});
                
                // When video pauses
                video.addEventListener('pause', () => {{
                    centerIcon.innerText = 'play_arrow';
                    item.classList.remove('is-playing');
                    
                    // Check if any videos are still playing globally
                    const anyPlaying = Array.from(document.querySelectorAll('video')).some(v => !v.paused);
                    if(!anyPlaying) {{
                        document.body.classList.remove('video-active');
                    }}
                }});

                // Mute toggle
                muteBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    video.muted = !video.muted;
                    muteIcon.innerText = video.muted ? 'volume_off' : 'volume_up';
                }});

                // Skip
                skipBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    video.currentTime = Math.min(video.currentTime + 5, video.duration || 0);
                }});
                
                // Fullscreen
                fullscreenBtn.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    if (video.requestFullscreen) {{
                        video.requestFullscreen();
                    }} else if (video.webkitRequestFullscreen) {{
                        video.webkitRequestFullscreen();
                    }}
                }});

                // Progress Bar
                video.addEventListener('timeupdate', () => {{
                    if(video.duration) {{
                        const percent = (video.currentTime / video.duration) * 100;
                        progressBar.style.width = percent + '%';
                    }}
                }});

                // Seek
                progressContainer.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    const rect = progressContainer.getBoundingClientRect();
                    const pos = (e.clientX - rect.left) / rect.width;
                    video.currentTime = pos * (video.duration || 0);
                }});
            }});
        }});
    </script>
</body>
</html>
'''

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(new_page)

print("Fixed performance and UX in projects.html")
