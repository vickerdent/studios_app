import subprocess

def run_tailwind_watch():
    """
    Runs TailwindCSS in watch mode for automatic recompilation.
    """
    command = [
        './tailwindcss',  # Make sure that this points to your tailwindcss file in your project.
        '-i', './the_messages/static/src/input.css',  # input
        '-o', './the_messages/static/src/output.css',  # output
        '--watch'
    ]
    subprocess.run(command)
    print('TailwindCSS watcher started.')

run_tailwind_watch()
