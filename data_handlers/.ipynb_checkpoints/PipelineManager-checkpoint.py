class PipelineManager:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def execute_steps(self, df):
        for step in self.steps:
            df = step.visit_huge_datasetbook(df)
        return df