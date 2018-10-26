import luigi
from le_extract_data import *
from le_fetch_data import *

class MainTask(luigi.WrapperTask):
    def requires(self):
        return ExportAllQueries()


if __name__ == '__main__':
    luigi.run(main_task_cls=MainTask,
              local_scheduler=False)

