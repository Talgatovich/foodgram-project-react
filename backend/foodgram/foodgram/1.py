from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent.parent
#TEMPLATES_DIR = Path(BASE_DIR / "frontend/src/pages/")
#shark = Path(Path.home(), "ocean", "animals", Path("fish", "shark.txt"))
#home = Path(Path.cwd())
#TEMPLATES_DIR = Path(home, "frontend", "src", "pages")
#TEMPLATES_DIR = Path(Path.home(), "wave.txt")
#F:\Dev\foodgram-project-react\frontend\src\pages
#print(home)
WORKDIR  = Path(Path.cwd())
TEMPLATES_DIR = Path(WORKDIR, "frontend", "src", "pages")
print(TEMPLATES_DIR)
