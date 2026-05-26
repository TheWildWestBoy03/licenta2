class PipelineManager:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def execute(self, df):
        for step in self.steps:
            df = step.process(df)
        return df