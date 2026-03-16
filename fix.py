with open('e:/pfppee/code.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:]

new_lines[188] = '<div class="flex flex-col items-start"><p class="text-3xl font-serif italic text-white">5+</p><p class="text-[10px] uppercase tracking-widest text-slate-500 mt-1">Years Creative Exp</p><div class="flex items-center gap-4 mt-3">\n'
new_lines[189] = lines[191]
new_lines[190] = lines[192]
new_lines[191] = lines[193]
new_lines[192] = '</div></div>\n'
new_lines[193] = lines[189]
new_lines[194] = '</div></div>\n'

with open('e:/pfppee/code.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Rewrite successful.')
