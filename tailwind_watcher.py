import subprocess

def run_tailwind_watch():
    """
    Runs TailwindCSS in watch mode for automatic recompilation.
    """
    command = [
        './tailwindcss',  # Make sure that this points to your tailwindcss file in your project.
        '-i', './sim/static/css/input.css',  # input
        '-o', './sim/static/css/output.css',  # output
        '--watch'
    ]
    subprocess.run(command)
    print('TailwindCSS watcher started.')

run_tailwind_watch()
