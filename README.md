# atlantis-helm-chart

Procore customizations to the upstream Atlantis Helm Chart repo.

# Docker Image
We have our own custom Dockerfile which adds some utilities on top of the upstream Atlantis image.
* The AWS CLI to the Atlantis image.
* The procore_terraform_wrapper.py script from this repo.

The image is built by CI and pushed to quay.io/procoredevops/atlantis-helm-chart/ using `procore-atlantis-vx.x.x-x.x.x` tags.

## Important Note on AWS CLI
The AWS CLI v2 is not currently (5/4/2021) compatible with Alpine based images. V2 requires glibc, and Alpine images do not have it. They use musl instead, and the AWS CLI v2 is not compatible with musl.

There's a workaround in this thread, but it's complicated.
https://github.com/aws/aws-cli/issues/4685

We could also investigate adding a second container to the atlantis pod that has the AWS CLI installed. We'd then just need to add a wrapper inside the atlantis container which redirects calls to `aws` to run in the other container.

# procore_terraform_wrapper

This script wraps calls to Terraform with the following goals:
1. Ensure any sensitive output is masked using `tfmask`, as the output is posted to GitHub by Atlantis.
2. Preserve the return code of `terraform` commands. Piping them to `tfmask` directly caused the loss of the original return code.
3. Reduce the amount of output from `terraform init` and `terraform plan` when the commands run without errors.

The last goal is acheived by:
1. Removing the messages when downloading external modules during `terraform init`
2. Removing the messages for the state refresh during `terraform plan`.

If the terraform commands return any errors or if the regular expressions used for reducing the output do not match, the full-length output will be printed. All output will still go through tfmask, regardless of errors.

## Usage
This script is intended to be used by Atlantis. You can run it locally for testing too.

```
usage: procore_terraform_wrapper.py [-h] --action {init,plan,apply} [--tf-version TF_VERSION] [--planfile PLANFILE] [--comment-args COMMENT_ARGS] [--debug]

Wraps calls to terraform and tfmask. For use with Atlantis.

optional arguments:
  -h, --help            show this help message and exit
  --action {init,plan,apply}
                        The Terraform command to perform.
  --tf-version TF_VERSION
                        Optional. The terraform version to use. Pass $ATLANTIS_TERRAFORM_VERSION to this.
  --planfile PLANFILE   Optional. Path to the planfile to use. Pass $PLANFILE to this.
  --comment-args COMMENT_ARGS
                        Optional. Extra args for terraform command. Pass $COMMENT_ARGS to this.
  --debug               Optional. Increase log level to debug.
```

For Atlantis usage, we will call this script as part of a custom workflow. See the `repoConfig` setting in the `values.yaml` file for the chart in this repo.

When running the script locally, just use it in place of the terraform command. You will need to install `tfmask` and have that available on your path before the script will work. See the `Dockerfile` in this repo for how to install `tfmask`.

For example, you might run this series of commands from within a terraform project directory (e.g. terraform-infra/us00/staging/security_kubernetes_cluster/):
```
aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action init
aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action plan
aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action apply
```

Here's some example output from local usage with a development cluster in terraform-infra:
```
tommckay@MACLAP-4ZYMD6R kubernetes_cluster % pwd
/Users/tommckay/Source/procore/terraform-infra/us00/staging/dev/kubernetes_cluster
tommckay@MACLAP-4ZYMD6R kubernetes_cluster % aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action init
2021-06-03 11:58:22,038:INFO:Running terraform init...
2021-06-03 11:58:22,038:INFO:Running command: terraform init -input=false -no-color
2021-06-03 11:59:45,960:INFO:Command completed. returncode=0
2021-06-03 11:59:45,961:INFO:Running command: tfmask
2021-06-03 11:59:46,030:INFO:Command completed. returncode=0
Initializing modules...
 Module downloads removed for brevity
Initializing the backend...

Successfully configured the backend "s3"! Terraform will automatically
use this backend unless the backend configuration changes.

Initializing provider plugins...
- Finding hashicorp/random versions matching ">= 2.1.*"...
(...snip other provider plugins...)

(...snip lots of output from terraform)

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

tommckay@MACLAP-4ZYMD6R kubernetes_cluster % aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action plan
2021-06-03 12:00:15,943:INFO:Running terraform plan...
2021-06-03 12:00:15,943:INFO:Running command: terraform plan -input=false -refresh -no-color -out plan.tfplan
2021-06-03 12:01:10,991:INFO:Command completed. returncode=0
2021-06-03 12:01:10,992:INFO:Running command: tfmask
2021-06-03 12:01:10,997:INFO:Command completed. returncode=0
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.
 State refresh removed for brevity
------------------------------------------------------------------------

No changes. Infrastructure is up-to-date.

This means that Terraform did not detect any differences between your
configuration and real physical resources that exist. As a result, no
actions need to be performed.


tommckay@MACLAP-4ZYMD6R kubernetes_cluster % aws-okta exec prnd_staging -- procore_terraform_wrapper.py --action apply
2021-06-03 12:01:55,915:INFO:Running terraform apply...
2021-06-03 12:01:55,915:INFO:Running command: terraform apply -no-color plan.tfplan
2021-06-03 12:02:08,397:INFO:Command completed. returncode=0
2021-06-03 12:02:08,397:INFO:Running command: tfmask
2021-06-03 12:02:08,403:INFO:Command completed. returncode=0

(...snip lots of output from terraform apply...)


Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

## Running tests
Run the tests after any changes to the python code.

```
cd procore_terraform_wrapper
pip3 install -r requirements.txt
pytest ./test/ -vvv
```