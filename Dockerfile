
FROM registry.access.redhat.com/ubi8/nodejs-18:1-81 as BASE
USER 0

ENV TF_PLUGIN_CACHE="${HOME}/.terraform.d/plugin-cache"
ENV TF_PROVIDER_AWS_VERSION="5.29.0"
ENV TF_PROVIDER_AWS_PATH="${TF_PLUGIN_CACHE}/registry.terraform.io/hashicorp/aws/${TF_PROVIDER_AWS_VERSION}/linux_amd64"


RUN \
    yum install -y yum-utils && \
    yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo && \
    yum -y install terraform && \
    yum install -y python3.11 && \
    yum install -y python3.11-pip.noarch && \
    npm install --global cdktf-cli@latest && \
    pip3 install pipenv

RUN mkdir -p ${TF_PROVIDER_AWS_PATH} && \
    curl -sfL https://releases.hashicorp.com/terraform-provider-aws/${TF_PROVIDER_AWS_VERSION}/terraform-provider-aws_${TF_PROVIDER_AWS_VERSION}_linux_amd64.zip \
    -o /tmp/package-aws-${TF_PROVIDER_AWS_VERSION}.zip && \
    unzip /tmp/package-aws-${TF_PROVIDER_AWS_VERSION}.zip -d ${TF_PROVIDER_AWS_PATH}/ && \
    rm /tmp/package-aws-${TF_PROVIDER_AWS_VERSION}.zip

COPY Pipfile Pipfile.lock /module/
RUN \
    chmod 777 /module && \
    cd /module && \
    pipenv sync

COPY conf/.terraformrc $HOME/
COPY main.py input.py cdktf.json entrypoint.sh /module/

ENTRYPOINT [ "bash", "/module/entrypoint.sh" ]
