FROM runatlantis/atlantis:v0.17.0

# Add AWS CLI v1 to the image
RUN apk add --no-cache \
        python3 \
        py3-pip \
    && pip3 install --upgrade pip \
    && pip3 install \
        awscli \
    && rm -rf /var/cache/apk/*

# Install tfmask
ADD https://github.com/cloudposse/tfmask/releases/download/0.7.0/tfmask_linux_amd64 /usr/bin/tfmask
RUN chmod +x /usr/bin/tfmask

# Install procore_terraform_wrapper.py
COPY procore_terraform_wrapper/procore_terraform_wrapper.py /usr/bin/
RUN chmod +x /usr/bin/procore_terraform_wrapper.py