import json
import time

import pygame

import synapse
import neuron

STEP = 50
HEIGHT = 600
WIDTH = 800
MAX_COORD_X = WIDTH/STEP - 1
MAX_COORD_Y = WIDTH/STEP - 1
CAPTION = "Neural Network Visualizer"
SLEEP_TIMER = 0.1
BLACK = (0, 0, 0)

FILE_NAME = "network.txt"

INPUT_X = 2
INPUT_Y = 1


class Main:
    def __init__(self):
        self._running = False
        self._displaySurf = None
        self._elementsList = []
        self._json = None

    def on_init(self):
        pygame.init()
        self._displaySurf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)

        pygame.display.set_caption(CAPTION)

        self._running = True

        f = open(FILE_NAME, "r")
        self._json = json.load(f)
        self.on_read_file(o=self._json)

        return True

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while self._running:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    self.on_cleanup()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        self.on_cleanup()

            self.on_loop()
            self.on_render()

            time.sleep(SLEEP_TIMER)

        return

    def on_render(self):
        self._displaySurf.fill(BLACK)
        for el in self._elementsList:
            el.draw(self._displaySurf)

        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.display.quit()
        pygame.quit()

    @staticmethod
    def on_loop():
        return

    def on_read_file(self, o):
        sensor_nodes = o['sensor_nodes']
        hidden_nodes = o['hidden_nodes']
        output_nodes = o['output_nodes']
        generations = o['generations']
        network = o['network']

        nodes = {}
        synapses_visited = []
        synapses = []

        # Sensor Nodes
        i = 0
        for n in sensor_nodes:
            _id = list(n.keys())[0]
            x = INPUT_X + 1
            y = i + INPUT_Y
            pos = (x*STEP, y*STEP)
            nodes[int(_id)] = pos

            for s in n[_id]["output_synapses"]:
                syn = {}
                for key, val in s.items():
                    if key in synapses_visited:
                        continue

                    if key == "other_end":
                        continue
                    else:
                        syn["a"] = int(_id)
                        syn["w"] = float(val)
                        syn["id"] = int(key)
                        syn["b"] = int(s["other_end"])
                        synapses_visited.append(key)
                if len(syn) > 0:
                    synapses.append(syn)

            i += 1

        # Output Nodes
        i = 0
        for n in output_nodes:
            _id = list(n.keys())[0]
            x = INPUT_X + 7
            y = i + INPUT_Y
            pos = (x * STEP, y * STEP)
            nodes[int(_id)] = pos

            for s in n[_id]["input_synapses"]:
                syn = {}
                for key, val in s.items():
                    if key in synapses_visited:
                        continue

                    if key == "other_end":
                        continue
                    else:
                        syn["b"] = int(_id)
                        syn["w"] = float(val)
                        syn["id"] = int(key)
                        syn["a"] = int(s["other_end"])
                        synapses_visited.append(key)
                if len(syn) > 0:
                    synapses.append(syn)

            i += 1

        # Hidden Nodes
        i = 0
        for n in hidden_nodes:
            _id = list(n.keys())[0]
            x = INPUT_X + 4
            y = i + INPUT_Y
            pos = (x * STEP, y * STEP)
            nodes[int(_id)] = pos

            for s in n[_id]["output_synapses"]:
                syn = {}
                for key, val in s.items():
                    if key in synapses_visited:
                        continue

                    if key == "other_end":
                        continue
                    else:
                        syn["a"] = int(_id)
                        syn["w"] = float(val)
                        syn["id"] = int(key)
                        syn["b"] = int(s["other_end"])
                        synapses_visited.append(key)
                if len(syn) > 0:
                    synapses.append(syn)

            for s in n[_id]["input_synapses"]:
                syn = {}
                for key, val in s.items():
                    if key in synapses_visited:
                        continue

                    if key == "other_end":
                        continue
                    else:
                        syn["b"] = int(_id)
                        syn["w"] = float(val)
                        syn["id"] = int(key)
                        syn["a"] = int(s["other_end"])
                        synapses_visited.append(key)
                if len(syn) > 0:
                    synapses.append(syn)

            i += 1

        for id_, pos in nodes.items():
            node = neuron.Neuron(id_, pos)
            self._elementsList.append(node)

        for el in synapses:
            _id = 0
            w = 0
            src = None
            dst = None
            for key, val in el.items():
                if key == "id":
                    _id = int(val)
                elif key == "w":
                    w = float(val)
                elif key == "a":
                    src = self.find_element(int(val))
                elif key == "b":
                    dst = self.find_element(int(val))

            c = (255, 0, 0)
            if abs(src.pos[0] - dst.pos[0]) > 3*STEP:
                c = (0, 255, 0)
            elif src.pos[0] == dst.pos[0]:
                c = (0, 0, 100)
            syn = synapse.Synapse(_id, src, dst, w, c=c)
            self._elementsList.append(syn)

        return

    def find_element(self, _id):
        for el in self._elementsList:
            if el.id == _id:
                return el

        return None

if __name__ == "__main__":
    main = Main()
    main.on_execute()
