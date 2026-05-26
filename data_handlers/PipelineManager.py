class PipelineManager:
    def __init__(self):
        self.steps = []

    def add_step(self, data_handler):
        self.steps.append(data_handler)

    def execute_steps(self, ingestor_instance, processing_chunk):
        for step in self.steps:
            processing_chunk = ingestor_instance.accept(step, processing_chunk)
