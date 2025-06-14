import PyInstaller.__main__
import sys
import os
import sounddevice

def build_exe():
    # Get the absolute path to the main script
    main_script = os.path.abspath(os.path.join('app', 'main.py'))
    
    # Find sounddevice package location
    sd_path = os.path.dirname(sounddevice.__file__)
    
    # Define PyInstaller arguments    args = [
        main_script,
        '--name=VibeScope',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        # Add paths to ensure all modules are included
        '--paths=.',
        '--add-data=venv/Lib/site-packages/sounddevice;sounddevice',
        '--hidden-import=numpy',
        '--hidden-import=sounddevice',
        '--hidden-import=pygame',
        '--hidden-import=sounddevice._sounddevice',
        '--hidden-import=_sounddevice',
        '--hidden-import=cffi',
        '--hidden-import=_cffi_backend',
        '--collect-all=sounddevice',
        '--collect-binaries=sounddevice',
        '--collect-data=sounddevice',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build_exe()
