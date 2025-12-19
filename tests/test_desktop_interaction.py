"""
桌面交互测试 - 截图、鼠标控制、键盘输入
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)
from ucloud_sandbox.desktop import Sandbox


def test_screenshot():
    """测试截图功能"""
    print("=" * 50)
    print("测试: 截图功能")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        # 等待桌面启动
        desktop.wait(3000)
        
        # 截图
        screenshot = desktop.screenshot()
        print(f"截图类型: {type(screenshot)}")
        print(f"截图大小: {len(screenshot)} bytes")
        
        assert screenshot is not None, "截图不应为空"
        assert len(screenshot) > 0, "截图大小应大于0"
        
        # 验证是PNG格式 (PNG magic bytes: 89 50 4E 47)
        assert screenshot[:4] == b'\x89PNG', "截图应为PNG格式"
        
        print("✓ 截图功能测试通过")
        return True
    finally:
        desktop.kill()


def test_mouse_move():
    """测试鼠标移动和获取位置"""
    print("\n" + "=" * 50)
    print("测试: 鼠标移动和获取位置")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 移动鼠标到指定位置
        target_x, target_y = 200, 300
        desktop.move_mouse(target_x, target_y)
        print(f"移动鼠标到: ({target_x}, {target_y})")
        
        # 获取当前鼠标位置
        x, y = desktop.get_cursor_position()
        print(f"当前鼠标位置: ({x}, {y})")
        
        # 验证位置 (允许小误差)
        assert abs(x - target_x) <= 5, f"X坐标应接近 {target_x}"
        assert abs(y - target_y) <= 5, f"Y坐标应接近 {target_y}"
        
        print("✓ 鼠标移动和获取位置测试通过")
        return True
    finally:
        desktop.kill()


def test_left_click():
    """测试左键点击"""
    print("\n" + "=" * 50)
    print("测试: 左键点击")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 在指定位置左键点击
        desktop.left_click(100, 100)
        print("在 (100, 100) 处左键点击")
        
        # 验证鼠标位置
        x, y = desktop.get_cursor_position()
        print(f"点击后鼠标位置: ({x}, {y})")
        
        assert abs(x - 100) <= 5, "X坐标应接近 100"
        assert abs(y - 100) <= 5, "Y坐标应接近 100"
        
        print("✓ 左键点击测试通过")
        return True
    finally:
        desktop.kill()


def test_double_click():
    """测试双击"""
    print("\n" + "=" * 50)
    print("测试: 双击")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 双击
        desktop.double_click(150, 150)
        print("在 (150, 150) 处双击")
        
        # 验证鼠标位置
        x, y = desktop.get_cursor_position()
        print(f"双击后鼠标位置: ({x}, {y})")
        
        assert abs(x - 150) <= 5, "X坐标应接近 150"
        assert abs(y - 150) <= 5, "Y坐标应接近 150"
        
        print("✓ 双击测试通过")
        return True
    finally:
        desktop.kill()


def test_right_click():
    """测试右键点击"""
    print("\n" + "=" * 50)
    print("测试: 右键点击")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 右键点击
        desktop.right_click(200, 200)
        print("在 (200, 200) 处右键点击")
        
        desktop.wait(500)
        
        # 按 Escape 关闭可能弹出的菜单
        desktop.press("escape")
        
        print("✓ 右键点击测试通过")
        return True
    finally:
        desktop.kill()


def test_keyboard_write():
    """测试键盘输入文本"""
    print("\n" + "=" * 50)
    print("测试: 键盘输入文本")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(3000)
        
        # 打开终端
        desktop.commands.run("xfce4-terminal &", background=True)
        desktop.wait(2000)
        
        # 输入文本
        test_text = "echo hello"
        desktop.write(test_text)
        print(f"输入文本: {test_text}")
        
        desktop.wait(500)
        
        print("✓ 键盘输入文本测试通过")
        return True
    finally:
        desktop.kill()


def test_keyboard_press():
    """测试按键操作"""
    print("\n" + "=" * 50)
    print("测试: 按键操作")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 测试单个按键
        desktop.press("enter")
        print("按下: Enter")
        
        desktop.press("escape")
        print("按下: Escape")
        
        # 测试组合键
        desktop.press(["ctrl", "c"])
        print("按下: Ctrl+C")
        
        desktop.press(["alt", "tab"])
        print("按下: Alt+Tab")
        
        print("✓ 按键操作测试通过")
        return True
    finally:
        desktop.kill()


def test_screen_size():
    """测试获取屏幕尺寸"""
    print("\n" + "=" * 50)
    print("测试: 获取屏幕尺寸")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 获取屏幕尺寸
        width, height = desktop.get_screen_size()
        print(f"屏幕尺寸: {width}x{height}")
        
        # 默认分辨率是 1024x768
        assert width == 1024, f"宽度应为 1024, 实际为 {width}"
        assert height == 768, f"高度应为 768, 实际为 {height}"
        
        print("✓ 获取屏幕尺寸测试通过")
        return True
    finally:
        desktop.kill()


def test_scroll():
    """测试滚动"""
    print("\n" + "=" * 50)
    print("测试: 滚动")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 向下滚动
        desktop.scroll(direction="down", amount=3)
        print("向下滚动 3 次")
        
        # 向上滚动
        desktop.scroll(direction="up", amount=2)
        print("向上滚动 2 次")
        
        print("✓ 滚动测试通过")
        return True
    finally:
        desktop.kill()


def test_drag():
    """测试拖拽"""
    print("\n" + "=" * 50)
    print("测试: 拖拽")
    print("=" * 50)
    
    desktop = Sandbox.create(template="desktop", timeout=300)
    try:
        desktop.wait(2000)
        
        # 从 (100, 100) 拖拽到 (300, 300)
        desktop.drag((100, 100), (300, 300))
        print("从 (100, 100) 拖拽到 (300, 300)")
        
        # 验证鼠标最终位置
        x, y = desktop.get_cursor_position()
        print(f"拖拽后鼠标位置: ({x}, {y})")
        
        assert abs(x - 300) <= 5, "X坐标应接近 300"
        assert abs(y - 300) <= 5, "Y坐标应接近 300"
        
        print("✓ 拖拽测试通过")
        return True
    finally:
        desktop.kill()


def run_all():
    """运行所有桌面交互测试"""
    from tests.conftest import run_tests_safely
    
    tests = [
        test_screenshot,
        test_mouse_move,
        test_left_click,
        test_double_click,
        test_right_click,
        test_keyboard_write,
        test_keyboard_press,
        test_screen_size,
        test_scroll,
        test_drag,
    ]
    run_tests_safely(tests, "desktop_interaction")


if __name__ == "__main__":
    run_all()
