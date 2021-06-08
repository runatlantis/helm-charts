#!/usr/bin/env python3
import logging
import subprocess
import argparse
import re
import sys
import shlex

# setup logging
logger = logging.getLogger(__name__)


def run_os_command(args: str, input: str = "") -> subprocess.CompletedProcess:
    """
    Runs and logs OS commands.
    :param args: The command to pass to subprocess
    :param input: An optional string to supply as input to the command.
    :return: CompletedProcess instance
    """
    logger.info(f'Running command: {args}')
    completed_process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, input=input, shell=True)
    logger.info(f'Command completed. returncode={completed_process.returncode}')
    logger.debug(completed_process)
    return completed_process


def reduce_init(input: str) -> str:
    """
    Removes unnecessary parts of the output of `terraform init`. This removes the messages related to downloading modules.
    :param input: The output from `terraform init`
    :return: The shortened `terraform init` output.
    """
    match = re.search(r"(.*?Initializing modules\.\.\.\n).+?(Initializing the backend\.\.\..+$)", input, re.DOTALL)
    if(match):
        input = match.expand(r"\1 Module downloads removed for brevity\n\2")
    else:
        logger.warning('Failed to match regex for terraform init replacement. Please report this to the Atlantis maintainers as a bug!')
    return input


def reduce_plan(input: str) -> str:
    """
    Removes unnecessary parts of the output of `terraform plan`. This removes the messages related to the state refresh.
    :param input: The output from `terraform plan`
    :return: The shortened `terraform plan` output.
    """
    match = re.search(r"(.+?persisted to local or remote state storage\.\n).+?(---------.+$)", input, re.DOTALL)
    if(match):
        input = match.expand(r"\1 State refresh removed for brevity\n\2")
    else:
        logger.warning('Failed to match regex for terraform init replacement. Please report this to the Atlantis maintainers as a bug!')
    return input


def terraform_init(atlantis_terraform_executable: str, comment_args: str) -> subprocess.CompletedProcess:
    """
    Runs `terraform init`. Will shorten the output if the command succeeds.
    :param atlantis_terraform_executable: The name of the terraform executable to use. (e.g. terraform0.13.6 or terraform)
    :param comment_args: Extra args to supply to terraform command
    :return: The CompletedProcess instance from running terraform.
    """
    # terraform$ATLANTIS_TERRAFORM_VERSION init -input=false -no-color
    logger.info('Running terraform init...')
    tf_completed_process = run_os_command(f'{atlantis_terraform_executable} init -input=false -no-color {comment_args}')
    # if terraform succeeded, run the reduce function to strip unnecessary output.
    if(tf_completed_process.returncode == 0):
        tf_completed_process.stdout = reduce_init(tf_completed_process.stdout)
    return tf_completed_process


def terraform_plan(atlantis_terraform_executable: str, comment_args: str, planfile: str) -> subprocess.CompletedProcess:
    """
    Runs `terraform plan`. Will shorten the output if the command succeeds.
    :param atlantis_terraform_executable: The name of the terraform executable to use. (e.g. terraform0.13.6 or terraform)
    :param comment_args: extra args to supply to terraform command
    :param planfile: Path to planfile to write to.
    :return: The CompletedProcess instance from running terraform.
    """
    # terraform$ATLANTIS_TERRAFORM_VERSION plan -input=false -refresh -no-color -out $PLANFILE | tfmask
    logger.info('Running terraform plan...')
    tf_completed_process = run_os_command(f'{atlantis_terraform_executable} plan -input=false -refresh -no-color -out {planfile} {comment_args}')
    # if terraform succeeded, run the reduce function to strip unnecessary output.
    if(tf_completed_process.returncode == 0):
        tf_completed_process.stdout = reduce_plan(tf_completed_process.stdout)
    return tf_completed_process


def terraform_apply(atlantis_terraform_executable: str, comment_args: str, planfile: str) -> subprocess.CompletedProcess:
    """
    Runs `terraform apply`.
    :param atlantis_terraform_executable: The name of the terraform executable to use. (e.g. terraform0.13.6 or terraform)
    :param comment_args: Extra args to supply to terraform command
    :param planfile: Path to planfile to apply.
    :return: The CompletedProcess instance from running terraform.
    """
    # terraform$ATLANTIS_TERRAFORM_VERSION apply -no-color $PLANFILE | tfmask
    logger.info('Running terraform apply...')
    return run_os_command(f'{atlantis_terraform_executable} apply -no-color {comment_args} {planfile}')


def quote_argument(input: str) -> str:
    """
    Quotes a command line argument using shlex
    :param input: Raw input from command line
    :return: Quoted command line argument.
    """
    if(input):
        input = shlex.quote(input)
    return input


def main_cli() -> int:
    """
    Main CLI method
    """
    # parse arguments
    parser = argparse.ArgumentParser(description='Wraps calls to terraform and tfmask. For use with Atlantis.')
    parser.add_argument('--action', choices=['init', 'plan', 'apply'], type=str, required=True, help='The Terraform command to perform.')
    parser.add_argument('--tf-version', type=str, default='', help='Optional. The terraform version to use. Pass $ATLANTIS_TERRAFORM_VERSION to this.')
    parser.add_argument('--planfile', type=str, default='default.tfplan', help='Optional. Path to the planfile to use. Pass $PLANFILE to this.')
    parser.add_argument('--comment-args', type=str, default='', help='Optional. Extra args for terraform command. Pass $COMMENT_ARGS to this.')
    parser.add_argument('--debug', action='store_true', help='Optional. Increase log level to debug.')
    args = parser.parse_args()

    # setup logging
    log_level = 'DEBUG' if args.debug else 'INFO'
    logging.basicConfig(level=log_level, format='%(asctime)s:%(levelname)s:%(message)s')

    # build commands from args
    atlantis_terraform_executable = f'terraform{quote_argument(args.tf_version)}'
    planfile = quote_argument(args.planfile)
    comment_args = ''
    if(args.comment_args):
        comment_args_split = args.comment_args.split(',')
        comment_args = ' '.join(comment_args_split)

    # run the right function based on args
    if(args.action == 'init'):
        tf_completed_process = terraform_init(atlantis_terraform_executable, comment_args)
    elif(args.action == 'plan'):
        tf_completed_process = terraform_plan(atlantis_terraform_executable, comment_args, planfile)
    elif(args.action == 'apply'):
        tf_completed_process = terraform_apply(atlantis_terraform_executable, comment_args, planfile)

    # run tfmask, piping the terraform_output to it
    tfmask_completed_process = run_os_command('tfmask', input=tf_completed_process.stdout)

    # print masked output from tfmask
    print(tfmask_completed_process.stdout)

    # return exit code based on return code of original terraform command
    return tf_completed_process.returncode


if __name__ == '__main__':
    sys.exit(main_cli())
