import glob
import os

files = glob.glob('ko/week6/*.py') + glob.glob('ko/week7/step*.py')

font_code = """
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
"""

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add font configuration
    if "Malgun Gothic" not in content:
        content = content.replace("import matplotlib.pyplot as plt", font_code.strip())
    
    # 2. Fix layout where necessary
    if "subplots_adjust" in content:
        # If it has subplots_adjust, it might have slider in the bottom.
        # Ensure top is adjusted to make room for Title.
        if "top=" not in content:
            content = content.replace("plt.subplots_adjust(bottom=0.25)", "plt.subplots_adjust(bottom=0.25, top=0.9)\nfig.tight_layout(rect=[0, 0.25, 1, 1])")
            # Wait, fig.tight_layout(rect=[0, 0.25, 1, 1]) is safer for Sliders at bottom!
            # Let's replace simple subplots_adjust with tight_layout with rect if it's not there.
            # Actually, just setting top=0.9 ensures title doesn't overlap.
            content = content.replace("plt.subplots_adjust(bottom=0.3)", "plt.subplots_adjust(bottom=0.3, top=0.9)")
            content = content.replace("plt.subplots_adjust(bottom=0.25)", "plt.subplots_adjust(bottom=0.25, top=0.9)")
            content = content.replace("plt.subplots_adjust(left=0.1, bottom=0.35)", "plt.subplots_adjust(left=0.1, bottom=0.35, top=0.9)")
    else:
        if "tight_layout" not in content:
            content = content.replace("plt.show()", "plt.tight_layout()\nplt.show()")
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files.")
