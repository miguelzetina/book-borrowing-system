FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Install packages
RUN apt-get update
RUN apt-get install apt-transport-https sudo -y

# Create User docker
RUN useradd -ms /bin/bash docker
RUN echo "docker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# create env valies
ENV PROJECT_DIR /home/docker/public
ENV MEDIA_DIR /home/docker/media
ENV REQUIREMENTS_DIR /home/docker/public/requirements

# Create Folders
RUN mkdir $PROJECT_DIR
RUN mkdir $MEDIA_DIR
RUN mkdir $REQUIREMENTS_DIR

# Change owner and group
RUN chown -R docker:docker $PROJECT_DIR
RUN chown -R docker:docker $MEDIA_DIR

# Copy requirements files
COPY src/requirements/base.txt /home/docker/public/requirements
COPY src/requirements/local.txt /home/docker/public/requirements

# Install pip requiremntes
RUN pip install -r $REQUIREMENTS_DIR/local.txt

# Init Project
WORKDIR /home/docker/public
USER docker