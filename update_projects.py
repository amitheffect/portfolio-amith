import re

projects_file = r'E:\pfppee\projects.html'

with open(projects_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Fullscreen button
skip_btn_html = '''<button class="skip-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                        <span class="material-symbols-outlined text-sm">skip_next</span>
                    </button>'''

fullscreen_btn_html = '''<button class="skip-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                        <span class="material-symbols-outlined text-sm">skip_next</span>
                    </button>
                    <button class="fullscreen-btn w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center border border-white/20 text-white hover:bg-white hover:text-midnight transition-colors">
                        <span class="material-symbols-outlined text-sm">fullscreen</span>
                    </button>'''

html = html.replace(skip_btn_html, fullscreen_btn_html)

# Replace the script
old_script_pattern = re.compile(r'<script>.*?</script>', re.DOTALL)

new_script = """<script>
        document.addEventListener('DOMContentLoaded', () => {
            const items = document.querySelectorAll('.gallery-item');
            
            items.forEach(item => {
                const video = item.querySelector('.cinematic-video');
                const centerBtn = item.querySelector('.center-play-btn');
                const centerIcon = centerBtn.querySelector('span');
                const muteBtn = item.querySelector('.mute-btn');
                const muteIcon = muteBtn.querySelector('span');
                const skipBtn = item.querySelector('.skip-btn');
                const fullscreenBtn = item.querySelector('.fullscreen-btn');
                const progressContainer = item.querySelector('.progress-container');
                const progressBar = item.querySelector('.progress-bar');
                
                // Get overlays to hide/show
                const topGradient = item.querySelector('.bg-gradient-to-t');
                const centerPlayWrapper = centerBtn.parentElement;
                const bottomControls = progressContainer.parentElement;

                const togglePlayingState = (isPlaying) => {
                    if (isPlaying) {
                        // Make others grayscale
                        items.forEach(otherItem => {
                            if (otherItem !== item) {
                                otherItem.classList.add('grayscale', 'opacity-50');
                            }
                        });
                        item.classList.remove('grayscale', 'opacity-50');
                    } else {
                        // Check if any other video is still playing
                        let anyPlaying = false;
                        items.forEach(otherItem => {
                            const v = otherItem.querySelector('video');
                            if (v && !v.paused) anyPlaying = true;
                        });
                        
                        if (!anyPlaying) {
                            items.forEach(otherItem => {
                                otherItem.classList.remove('grayscale', 'opacity-50');
                            });
                        } else {
                            item.classList.add('grayscale', 'opacity-50');
                        }
                    }
                };

                // Play/Pause toggle
                centerBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    if(video.paused) {
                        video.play();
                    } else {
                        video.pause();
                    }
                });

                // Update icon on actual video state change (in case of auto-pause etc)
                video.addEventListener('play', () => {
                    centerIcon.innerText = 'pause';
                    togglePlayingState(true);
                });
                
                video.addEventListener('pause', () => {
                    centerIcon.innerText = 'play_arrow';
                    togglePlayingState(false);
                    // Ensure UI is visible when paused
                    topGradient.classList.remove('opacity-0');
                    topGradient.classList.add('opacity-100');
                    centerPlayWrapper.classList.remove('opacity-0');
                    centerPlayWrapper.classList.add('opacity-100');
                    bottomControls.classList.remove('opacity-0');
                    bottomControls.classList.add('opacity-100');
                });
                
                video.addEventListener('ended', () => {
                    centerIcon.innerText = 'play_arrow';
                    togglePlayingState(false);
                    // Show UI on end
                    topGradient.classList.remove('opacity-0');
                    topGradient.classList.add('opacity-100');
                    centerPlayWrapper.classList.remove('opacity-0');
                    centerPlayWrapper.classList.add('opacity-100');
                    bottomControls.classList.remove('opacity-0');
                    bottomControls.classList.add('opacity-100');
                });

                // Mute toggle
                muteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    video.muted = !video.muted;
                    muteIcon.innerText = video.muted ? 'volume_off' : 'volume_up';
                });

                // Skip 5 seconds
                skipBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    video.currentTime = Math.min(video.currentTime + 5, video.duration);
                });
                
                // Fullscreen
                if (fullscreenBtn) {
                    fullscreenBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        if (video.requestFullscreen) {
                            video.requestFullscreen();
                        } else if (video.webkitRequestFullscreen) { /* Safari */
                            video.webkitRequestFullscreen();
                        } else if (video.msRequestFullscreen) { /* IE11 */
                            video.msRequestFullscreen();
                        }
                    });
                }

                // Update progress bar
                video.addEventListener('timeupdate', () => {
                    if(video.duration) {
                        const percent = (video.currentTime / video.duration) * 100;
                        progressBar.style.width = percent + '%';
                    }
                });

                // Seek on progress bar click
                progressContainer.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const rect = progressContainer.getBoundingClientRect();
                    const pos = (e.clientX - rect.left) / rect.width;
                    video.currentTime = pos * video.duration;
                });
                
                // Handle UI visibility on hover
                item.addEventListener('mouseenter', () => {
                    // Always show UI on hover
                    topGradient.classList.remove('opacity-0');
                    topGradient.classList.add('opacity-100');
                    centerPlayWrapper.classList.remove('opacity-0');
                    centerPlayWrapper.classList.add('opacity-100');
                    bottomControls.classList.remove('opacity-0');
                    bottomControls.classList.add('opacity-100');
                });

                item.addEventListener('mouseleave', () => {
                    if(!video.paused) {
                        // Hide UI if playing and mouse leaves
                        topGradient.classList.remove('opacity-100');
                        topGradient.classList.add('opacity-0');
                        centerPlayWrapper.classList.remove('opacity-100');
                        centerPlayWrapper.classList.add('opacity-0');
                        bottomControls.classList.remove('opacity-100');
                        bottomControls.classList.add('opacity-0');
                    } else {
                        // Keep hidden if it was just a quick pass-over without playing
                        // Actually, the group-hover handles hiding it via CSS normally,
                        // but since we override with JS classes above, let's clean up
                        topGradient.classList.remove('opacity-100');
                        topGradient.classList.add('opacity-0');
                        centerPlayWrapper.classList.remove('opacity-100');
                        centerPlayWrapper.classList.add('opacity-0');
                        bottomControls.classList.remove('opacity-100');
                        bottomControls.classList.add('opacity-0');
                    }
                });
            });
        });
    </script>"""

html = old_script_pattern.sub(new_script, html, count=1)

# Ensure the gallery items transition for grayscale works properly.
# We need to add transition-all duration-700 to gallery-item if it's not there.
# The original class had: bg-midnight-light rounded-2xl overflow-hidden break-inside-avoid mb-6 shadow-2xl border border-white/5
html = html.replace('gallery-item group relative bg-midnight-light', 'gallery-item group relative bg-midnight-light transition-all duration-700')

with open(projects_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated script and fullscreen button in projects.html")
