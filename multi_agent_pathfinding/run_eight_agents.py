"""
一键运行八个智能体演示
"""

import subprocess
import sys
import os


def install_dependencies():
    """安装必要的依赖"""
    print("Checking dependencies...")

    try:
        import numpy
        import matplotlib
        print("✓ numpy and matplotlib already installed")
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "matplotlib"])
        print("✓ Dependencies installed")

    # 可选：询问是否安装动画保存支持
    choice = input("\nDo you want to install animation saving support? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
            print("✓ Pillow installed for GIF support")
        except:
            print("✗ Failed to install Pillow")

        choice2 = input("Install ffmpeg for MP4 support? (y/n): ").strip().lower()
        if choice2 == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "ffmpeg-python"])
                print("✓ ffmpeg-python installed")
            except:
                print("✗ Failed to install ffmpeg-python")
                print("  You can install ffmpeg manually:")
                print("  - Windows: Download from https://ffmpeg.org/")
                print("  - macOS: brew install ffmpeg")
                print("  - Linux: sudo apt-get install ffmpeg")


def check_files():
    """检查必要的文件"""
    print("\nChecking files...")

    required_files = [
        "Berlin_1_256.map",
        "main.py",
        "demo.py",
        "config.py",
        "environment/__init__.py",
        "environment/map_loader.py",
        "environment/grid.py",
        "environment/agent_manager.py",
        "algorithms/__init__.py",
        "algorithms/astar.py",
        "algorithms/cbs.py",
        "algorithms/constraints.py",
        "utils/__init__.py",
        "utils/visualization.py",
        "utils/metrics.py",
        "utils/logger.py"
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("✗ Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✓ All required files found")
        return True


def main():
    """主函数"""
    print("=" * 60)
    print("8-AGENT PATH PLANNING SYSTEM LAUNCHER")
    print("=" * 60)

    # 检查依赖
    install_dependencies()

    # 检查文件
    if not check_files():
        print("\nSome files are missing. Please ensure all files are in the correct location.")
        input("Press Enter to exit...")
        return

    print("\n" + "=" * 60)
    print("SELECT PROGRAM TO RUN:")
    print("=" * 60)
    print("1. 🎯 Main Program (8 agents with CBS algorithm)")
    print("2. 🎮 Interactive Demo (menu-driven experience)")
    print("3. ⚡ Fast Demo (straight to animation)")
    print("4. 🧪 Run Tests")
    print("5. 🚪 Exit")
    print("=" * 60)

    choice = input("\nSelect an option (1-5): ").strip()

    if choice == "1":
        print("\nRunning main program...")
        subprocess.call([sys.executable, "main.py"])
    elif choice == "2":
        print("\nRunning interactive demo...")
        subprocess.call([sys.executable, "demo.py"])
    elif choice == "3":
        print("\nRunning fast demo...")
        # 修改配置为快速模式
        with open("config.py", "r") as f:
            config_content = f.read()

        # 更新配置
        config_content = config_content.replace('ANIMATION_INTERVAL = 100', 'ANIMATION_INTERVAL = 50')
        config_content = config_content.replace('NUM_AGENTS = 8', 'NUM_AGENTS = 8')

        with open("config.py", "w") as f:
            f.write(config_content)

        subprocess.call([sys.executable, "demo.py"])

        # 恢复配置
        config_content = config_content.replace('ANIMATION_INTERVAL = 50', 'ANIMATION_INTERVAL = 100')
        with open("config.py", "w") as f:
            f.write(config_content)
    elif choice == "4":
        print("\nRunning tests...")
        subprocess.call([sys.executable, "-m", "pytest", "tests/", "-v"])
    elif choice == "5":
        print("\nExiting...")
    else:
        print("\nInvalid choice. Running main program...")
        subprocess.call([sys.executable, "main.py"])

    print("\n" + "=" * 60)
    print("PROGRAM FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()