import glob
from pathlib import Path

files = glob.glob("../org/roam/*.org")

print("Found files:")
print(files)

with open('build.ninja', 'w') as ninja_file:
    ninja_file.write("""
rule org2md
  command = emacs --batch -l ~/.emacs.d/batch.el -l publish.el --eval \"(jethro/publish \\"$in\\")"
  description = org2md $in
""")

    for f in files:
        path = Path(f)
        output_file = f"content/posts/{path.with_suffix('.md').name}"
        ninja_file.write(f"""
build {output_file}: org2md {path.as_posix()}
""")

import subprocess
subprocess.call(["ninja"])
