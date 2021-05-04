# procore-atlantis
Dockerfile which adds the AWS cli to the Atlantis image.

# Notes
The AWS CLI v2 is not currently (5/4/2021) compatible with Alpine based images. V2 requires glibc, and Alpine images do not have it. They use musl instead, and the AWS CLI v2 is not compatible with musl.

There's a workaround in this thread, but it's complicated.
https://github.com/aws/aws-cli/issues/4685

We could also investigate adding a second container to the atlantis pod that has the AWS CLI installed. We'd then just need to add a wrapper inside the atlantis container which redirects calls to `aws` to run in the other container.