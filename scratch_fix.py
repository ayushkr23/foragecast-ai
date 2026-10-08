with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<p class="main-title">', '<p style="font-size: 4.5rem; font-weight: 900; background: -webkit-linear-gradient(45deg, #81C784, #2E7D32); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; line-height: 1.2;">')
content = content.replace('<p class="sub-title">', '<p style="font-size: 1.2rem; color: #888; margin-bottom: 40px;">')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
