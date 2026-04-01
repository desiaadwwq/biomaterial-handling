import os
import glob
import re

directories = [
    r'c:\Users\ryudongsoo\OneDrive\RyuVault\1. Projects\2026년1학기강의\생물자원가공공학및실습\biomaterial-handling\en\week6',
    r'c:\Users\ryudongsoo\OneDrive\RyuVault\1. Projects\2026년1학기강의\생물자원가공공학및실습\biomaterial-handling\en\week7',
    r'c:\Users\ryudongsoo\OneDrive\RyuVault\1. Projects\2026년1학기강의\생물자원가공공학및실습\biomaterial-handling\en\week9'
]

font_setup = """import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False"""

emoji_map = {
    '✅': 'O',
    '❌': 'X',
    '⚠️': '!',
    '🎛️': '',
    '🔬': '',
    '🔩': '',
    '🎨': '',
    '📊': '',
    '₀': '_0',
    '₁': '_1',
    '₂': '_2',
    'ᵣ': '_r'
}

for d in directories:
    for filepath in glob.glob(os.path.join(d, '*.py')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Add font setup if not present
        if "plt.rcParams['font.family'] = 'Malgun Gothic'" not in content:
            content = re.sub(r'import matplotlib\.pyplot as plt', font_setup, content)

        # 2. Fix y=1.02 in suptitle
        content = re.sub(r'(\n\s*fig\.suptitle\([^)]*),\s*y=1\.02\)', r'\1)', content)
        
        # 3. Change top=0.92 to top=0.88
        content = content.replace('top=0.92', 'top=0.88')

        # 4. Remove emojis and convert subscripts
        for emoji, replacement in emoji_map.items():
            content = content.replace(emoji, replacement)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("Patch complete for en/ scripts.")
