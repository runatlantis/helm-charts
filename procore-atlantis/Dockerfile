FROM runatlantis/atlantis:v0.17.0

# Add AWS CLI v1 to the image
RUN apk add --no-cache \
        python3 \
        py3-pip \
    && pip3 install --upgrade pip \
    && pip3 install \
        awscli \
    && rm -rf /var/cache/apk/*