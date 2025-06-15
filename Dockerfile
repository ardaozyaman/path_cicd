FROM jenkins/jenkins:lts
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv
RUN jenkins-plugin-cli --plugins workflow-aggregator git github htmlpublisher
USER jenkins
