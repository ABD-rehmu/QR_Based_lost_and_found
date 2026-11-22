import re

def audit_icons():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html1 = f.read()
    with open('static/finder.html', 'r', encoding='utf-8') as f:
        html2 = f.read()
    with open('static/print_tags.html', 'r', encoding='utf-8') as f:
        html3 = f.read()
    with open('static/js/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    all_text = html1 + html2 + html3 + js
    icons = set(re.findall(r'data-lucide=[\'"]([^\'"]+)[\'"]', all_text))
    print(f"Total unique Lucide icons used: {len(icons)}")
    print("Icons:", sorted(icons))

if __name__ == '__main__':
    audit_icons()
