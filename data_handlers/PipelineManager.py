class PipelineManager:
    def __init__(self):
        self.steps = []

    def add_step(self, data_handler):
        self.steps.append(data_handler)

    def execute_steps(self, ingestor):
        for step in self.steps:
            ingestor.accept(step)