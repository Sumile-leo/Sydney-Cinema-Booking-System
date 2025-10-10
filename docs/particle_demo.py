"""
粒子效果演示程序
展示纯代码实现的5种元素粒子效果
按1-5键切换不同元素，鼠标拖拽绘制魔法！
"""

import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QFont


class Particle:
    """基础粒子类"""
    def __init__(self, x, y, color, size=5):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = color
        self.size = size
        self.lifetime = 60
        self.max_lifetime = 60
        self.alpha = 255
    
    def update(self):
        """更新粒子状态"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制粒子"""
        painter.setBrush(QColor(self.color[0], self.color[1], self.color[2], self.alpha))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(self.x - self.size/2), int(self.y - self.size/2), 
                           self.size, self.size)


class FireParticle(Particle):
    """🔥 火焰粒子"""
    def __init__(self, x, y):
        colors = [(255, 50, 0), (255, 100, 0), (255, 200, 0)]
        color = random.choice(colors)
        super().__init__(x, y, color, size=random.randint(4, 10))
        self.vy = random.uniform(-3, -1)  # 向上飘
        self.vx = random.uniform(-0.5, 0.5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # 颜色从红到黄渐变
        progress = 1 - (self.lifetime / self.max_lifetime)
        self.color = (255, int(50 + 150 * progress), 0)
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制发光的火焰"""
        # 外层光晕（橙色）
        painter.setBrush(QColor(255, 100, 0, self.alpha // 3))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(self.x - self.size), int(self.y - self.size), 
                           self.size * 2, self.size * 2)
        
        # 中层（橙黄色）
        painter.setBrush(QColor(255, 150, 0, self.alpha // 2))
        painter.drawEllipse(int(self.x - self.size*0.7), int(self.y - self.size*0.7), 
                           int(self.size * 1.4), int(self.size * 1.4))
        
        # 核心（亮黄色）
        painter.setBrush(QColor(*self.color, self.alpha))
        painter.drawEllipse(int(self.x - self.size/2), int(self.y - self.size/2), 
                           self.size, self.size)


class WaterParticle(Particle):
    """💧 水滴粒子"""
    def __init__(self, x, y):
        super().__init__(x, y, (50, 150, 255), size=random.randint(3, 7))
        self.vy = random.uniform(0.5, 2)  # 向下落
        self.vx = random.uniform(-1, 1)
        self.gravity = 0.15
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # 重力加速
        self.lifetime -= 1
        self.alpha = int(200 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制水滴"""
        # 主体（半透明蓝色）
        painter.setBrush(QColor(50, 150, 255, self.alpha))
        painter.setPen(Qt.NoPen)
        # 椭圆形水滴
        painter.drawEllipse(int(self.x - self.size/2), int(self.y - self.size/2), 
                           self.size, int(self.size * 1.3))
        
        # 高光
        painter.setBrush(QColor(200, 230, 255, self.alpha))
        painter.drawEllipse(int(self.x - self.size/4), int(self.y - self.size/3), 
                           self.size // 2, self.size // 2)


class ThunderParticle:
    """⚡ 雷电粒子"""
    def __init__(self, x1, y1, x2, y2):
        self.points = self.generate_lightning(x1, y1, x2, y2)
        self.lifetime = 8
        self.alpha = 255
    
    def generate_lightning(self, x1, y1, x2, y2):
        """生成闪电路径"""
        points = [(x1, y1)]
        segments = 10
        
        for i in range(1, segments):
            progress = i / segments
            x = x1 + (x2 - x1) * progress
            y = y1 + (y2 - y1) * progress
            
            # 添加随机偏移
            offset = random.randint(-15, 15)
            points.append((x + offset, y))
        
        points.append((x2, y2))
        return points
    
    def update(self):
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / 8))
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制闪电"""
        if len(self.points) < 2:
            return
        
        # 外层光晕（淡黄色）
        pen = QPen(QColor(255, 255, 100, self.alpha // 3))
        pen.setWidth(8)
        painter.setPen(pen)
        for i in range(len(self.points) - 1):
            painter.drawLine(int(self.points[i][0]), int(self.points[i][1]),
                           int(self.points[i+1][0]), int(self.points[i+1][1]))
        
        # 中层（亮黄色）
        pen = QPen(QColor(255, 255, 150, self.alpha // 2))
        pen.setWidth(4)
        painter.setPen(pen)
        for i in range(len(self.points) - 1):
            painter.drawLine(int(self.points[i][0]), int(self.points[i][1]),
                           int(self.points[i+1][0]), int(self.points[i+1][1]))
        
        # 核心（白色）
        pen = QPen(QColor(255, 255, 255, self.alpha))
        pen.setWidth(2)
        painter.setPen(pen)
        for i in range(len(self.points) - 1):
            painter.drawLine(int(self.points[i][0]), int(self.points[i][1]),
                           int(self.points[i+1][0]), int(self.points[i+1][1]))


class IceParticle(Particle):
    """❄️ 冰晶粒子"""
    def __init__(self, x, y):
        super().__init__(x, y, (180, 220, 255), size=random.randint(4, 9))
        self.vy = random.uniform(0.3, 1)
        self.vx = random.uniform(-0.5, 0.5)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed
        self.lifetime -= 1
        self.alpha = int(230 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制旋转的冰晶"""
        painter.save()
        painter.translate(int(self.x), int(self.y))
        painter.rotate(self.rotation)
        
        # 绘制六边形雪花
        pen = QPen(QColor(180, 220, 255, self.alpha))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # 六条主线
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = int(self.size * math.cos(rad))
            y = int(self.size * math.sin(rad))
            painter.drawLine(0, 0, x, y)
            
            # 小分支
            branch_x = int(self.size * 0.6 * math.cos(rad))
            branch_y = int(self.size * 0.6 * math.sin(rad))
            side_rad1 = math.radians(angle + 30)
            side_rad2 = math.radians(angle - 30)
            painter.drawLine(branch_x, branch_y, 
                           branch_x + int(self.size * 0.3 * math.cos(side_rad1)),
                           branch_y + int(self.size * 0.3 * math.sin(side_rad1)))
            painter.drawLine(branch_x, branch_y,
                           branch_x + int(self.size * 0.3 * math.cos(side_rad2)),
                           branch_y + int(self.size * 0.3 * math.sin(side_rad2)))
        
        # 中心亮点
        painter.setBrush(QColor(255, 255, 255, self.alpha))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-2, -2, 4, 4)
        
        painter.restore()


class WindParticle(Particle):
    """🌪️ 风粒子"""
    def __init__(self, x, y):
        super().__init__(x, y, (200, 200, 200), size=random.randint(2, 5))
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.trail = []
        self.max_trail = 8
    
    def update(self):
        self.trail.append((self.x, self.y, self.alpha))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.alpha = int(180 * (self.lifetime / self.max_lifetime))
        
        return self.lifetime > 0
    
    def draw(self, painter):
        """绘制带拖尾的风粒子"""
        # 绘制拖尾
        for i, (x, y, alpha) in enumerate(self.trail):
            trail_alpha = int(alpha * (i / len(self.trail)))
            trail_size = int(self.size * (i / len(self.trail)))
            if trail_size > 0:
                painter.setBrush(QColor(200, 200, 200, trail_alpha))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(x - trail_size/2), int(y - trail_size/2),
                                   trail_size, trail_size)
        
        # 主粒子
        painter.setBrush(QColor(230, 230, 230, self.alpha))
        painter.drawEllipse(int(self.x - self.size/2), int(self.y - self.size/2),
                           self.size, self.size)


class ParticleDemo(QWidget):
    """粒子效果演示窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 粒子效果演示 - Particle Demo")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #1a1a2e;")
        
        self.particles = []
        self.current_element = "fire"
        self.mouse_pressed = False
        self.last_mouse_pos = None
        
        # 定时器（60 FPS）
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(16)  # ~60 FPS
        
        self.element_names = {
            "fire": "🔥 火焰",
            "water": "💧 水流",
            "thunder": "⚡ 雷电",
            "ice": "❄️ 冰晶",
            "wind": "🌪️ 风"
        }
    
    def keyPressEvent(self, event):
        """键盘事件 - 切换元素"""
        key_map = {
            Qt.Key_1: "fire",
            Qt.Key_2: "water",
            Qt.Key_3: "thunder",
            Qt.Key_4: "ice",
            Qt.Key_5: "wind"
        }
        
        if event.key() in key_map:
            self.current_element = key_map[event.key()]
        elif event.key() == Qt.Key_C:
            self.particles.clear()  # 清空
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        self.mouse_pressed = True
        self.last_mouse_pos = event.pos()
        self.spawn_particles(event.x(), event.y())
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        self.mouse_pressed = False
        self.last_mouse_pos = None
    
    def mouseMoveEvent(self, event):
        """鼠标移动 - 绘制粒子"""
        if self.mouse_pressed:
            self.spawn_particles(event.x(), event.y())
            self.last_mouse_pos = event.pos()
    
    def spawn_particles(self, x, y):
        """生成粒子"""
        count = 5  # 每次生成5个粒子
        
        if self.current_element == "fire":
            for _ in range(count):
                self.particles.append(FireParticle(x, y))
        
        elif self.current_element == "water":
            for _ in range(count):
                self.particles.append(WaterParticle(x, y))
        
        elif self.current_element == "thunder":
            # 雷电需要起点和终点
            if self.last_mouse_pos:
                self.particles.append(ThunderParticle(
                    self.last_mouse_pos.x(), self.last_mouse_pos.y(),
                    x, y
                ))
        
        elif self.current_element == "ice":
            for _ in range(count):
                self.particles.append(IceParticle(x, y))
        
        elif self.current_element == "wind":
            for _ in range(count):
                self.particles.append(WindParticle(x, y))
    
    def update_particles(self):
        """更新所有粒子"""
        # 更新粒子状态，移除死亡粒子
        self.particles = [p for p in self.particles if p.update()]
        
        # 重绘
        self.update()
    
    def paintEvent(self, event):
        """绘制"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        
        # 绘制所有粒子
        for particle in self.particles:
            particle.draw(painter)
        
        # 绘制UI信息
        self.draw_ui(painter)
    
    def draw_ui(self, painter):
        """绘制UI信息"""
        # 标题
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        painter.drawText(20, 40, "🎨 粒子效果演示")
        
        # 当前元素
        painter.setFont(QFont("Arial", 16))
        painter.drawText(20, 70, f"当前元素: {self.element_names[self.current_element]}")
        
        # 粒子数量
        painter.drawText(20, 95, f"粒子数量: {len(self.particles)}")
        
        # 操作说明
        painter.setFont(QFont("Arial", 12))
        y_offset = 130
        instructions = [
            "操作说明:",
            "• 按 1-5 切换元素",
            "• 鼠标拖拽绘制魔法",
            "• 按 C 清空屏幕",
            "",
            "1 = 🔥 火焰",
            "2 = 💧 水流", 
            "3 = ⚡ 雷电",
            "4 = ❄️ 冰晶",
            "5 = 🌪️ 风"
        ]
        
        for instruction in instructions:
            painter.drawText(20, y_offset, instruction)
            y_offset += 20


def main():
    app = QApplication(sys.argv)
    demo = ParticleDemo()
    demo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

