FROM public.ecr.aws/lambda/python:3.8


# Required for lxml
RUN yum install -y yum-utils
RUN yum groupinstall -y "Development Tools"
RUN yum install -y gcc gcc-c++ libxml2 libxslt-dev

COPY ./ ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
CMD [ "main.handler" ]