import logging
from ..procore_terraform_wrapper import reduce_init, reduce_plan

# setup logging
logging.basicConfig(level='INFO', format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def run_reduce(reduce_func, original_file_name, reduced_file_name):
    original_file = open(original_file_name)
    original_file_contents = original_file.read()
    replaced = reduce_func(original_file_contents)
    reduced_file = open(reduced_file_name)
    reduced_file_contents = reduced_file.read()
    logger.warning(f'Expected:\n{reduced_file_contents}')
    logger.warning(f'Actual:\n{replaced}')
    assert replaced == reduced_file_contents


def test_reduce_init():
    run_reduce(reduce_init, 'test/init_nocolor_output.txt', 'test/init_nocolor_output_reduced.txt')


def test_reduce_plan():
    run_reduce(reduce_plan, 'test/plan_nocolor_output.txt', 'test/plan_nocolor_output_reduced.txt')
