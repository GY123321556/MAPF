"""
基本测试
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np

from environment.map_loader import MapLoader
from environment.grid import GridEnvironment
from environment.agent_manager import AgentManager


class TestMapLoader(unittest.TestCase):
    """测试地图加载器"""

    def test_load_map(self):
        """测试地图加载"""
        map_loader = MapLoader("Berlin_1_256.map")
        grid = map_loader.load_map()

        self.assertIsNotNone(grid)
        self.assertEqual(grid.shape, (256, 256))
        self.assertIn(0, grid)  # 应该有可通行区域
        self.assertIn(1, grid)  # 应该有障碍物

    def test_free_cells(self):
        """测试获取可通行单元格"""
        map_loader = MapLoader("Berlin_1_256.map")
        grid = map_loader.load_map()
        free_cells = map_loader.get_free_cells()

        self.assertGreater(len(free_cells), 0)

        # 检查所有单元格都是可通行的
        for x, y in free_cells[:10]:  # 只检查前10个
            self.assertEqual(grid[x, y], 0)


class TestGridEnvironment(unittest.TestCase):
    """测试网格环境"""

    def setUp(self):
        """设置测试环境"""
        self.grid = np.array([
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ])
        self.env = GridEnvironment(self.grid)

    def test_get_neighbors(self):
        """测试获取邻居"""
        neighbors = self.env.get_neighbors((0, 0, 0))

        # 从(0,0)应该可以移动到(0,1)和(1,0)
        expected = [(0, 0, 1), (0, 1, 1), (1, 0, 1)]

        self.assertEqual(len(neighbors), 3)
        for neighbor in expected:
            self.assertIn(neighbor, neighbors)

    def test_manhattan_distance(self):
        """测试曼哈顿距离计算"""
        distance = self.env.get_manhattan_distance((0, 0), (3, 3))
        self.assertEqual(distance, 6)

        distance = self.env.get_manhattan_distance((1, 2), (1, 2))
        self.assertEqual(distance, 0)

    def test_check_collision(self):
        """测试碰撞检测"""
        self.assertTrue(self.env.check_collision((1, 1), (1, 1)))
        self.assertFalse(self.env.check_collision((0, 0), (1, 1)))


class TestAgentManager(unittest.TestCase):
    """测试智能体管理器"""

    def setUp(self):
        """设置测试环境"""
        self.grid = np.zeros((10, 10), dtype=int)
        self.agent_manager = AgentManager(self.grid)

    def test_generate_agents(self):
        """测试生成智能体"""
        agents = self.agent_manager.generate_random_agents(3, min_distance=2)

        self.assertEqual(len(agents), 3)

        # 检查所有智能体都有不同的起点和终点
        starts = [agent.start for agent in agents]
        goals = [agent.goal for agent in agents]

        self.assertEqual(len(set(starts)), 3)
        self.assertEqual(len(set(goals)), 3)

        # 检查起点和终点在网格范围内
        for agent in agents:
            self.assertTrue(0 <= agent.start[0] < 10)
            self.assertTrue(0 <= agent.start[1] < 10)
            self.assertTrue(0 <= agent.goal[0] < 10)
            self.assertTrue(0 <= agent.goal[1] < 10)


if __name__ == "__main__":
    unittest.main()