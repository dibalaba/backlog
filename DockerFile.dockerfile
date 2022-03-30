# Dockerizing Python and MongoDB
# Based on ubuntu:latest, installs MongoDB following the instructions from:
# http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
# INSTRUCTIONS:
# - Create the contianer:
#   > docker build -t ubuntu_pymongo .
# - Create a folder to share your project in your host with the container. Ex: ~/shared
# - Run the next command (need the route of the created shared folder), this command access to the bash of container:
#   > docker run -v /c/Users/Jhonny/Documents/vm_share/mongoDB/shared:/data/code -t -i -p 27019:27017 ubuntu_pymongo
# - To open another bash console run the command: 
#   > docker exec -it <id_contenedor> bash
# - Run the mongo database:
#   > mongod
# - To connect compass or another gui with mongo use the IP of docker: 192.168.99.100 and the port 27019, or another that you indicate in the command
# https://stackoverflow.com/questions/33558506/how-to-create-a-mongo-docker-image-with-default-collections-and-data
# https://stackoverflow.com/questions/43575295/how-to-import-data-to-mongodb-container-and-creating-an-image

FROM       ubuntu:18.04
WORKDIR /backlog
USER root


# Installation:
COPY . /backlog


RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN set -ex \
	&& apk add --no-cache --virtual .fetch-deps \
		gnupg \
		tar \
		xz 

	
RUN apk add --no-cache --virtual .build-deps  \
		bluez-dev \
		bzip2-dev \
		coreutils \
		dpkg-dev dpkg \
		expat-dev \
		findutils \
		gcc \
		gdbm-dev \
		libc-dev \
		libffi-dev \
		libnsl-dev \
		libtirpc-dev \
		linux-headers \
		make \
		ncurses-dev \
		openssl-dev \
		pax-utils \
		readline-dev \
		sqlite-dev \
		tcl-dev \
		tk \
		tk-dev \
		util-linux-dev \
		xz-dev \
		zlib-dev \
# add build deps before removing fetch deps in case there's overlap
	&& apk del --no-network .fetch-deps \
	&& python3 --version

# make some useful symlinks that are expected to exist



# Import MongoDB public GPG key AND create a MongoDB list file
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv 7F0CEB10
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/10gen.list

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Create the MongoDB data directory
RUN mkdir -p /data/code



# Expose port #27017 from the container to the host
EXPOSE 27017

RUN pip3 install pymongo \
&& pip3 install json \
&& pip ast \
&& pip3 install bson \
&& pip3 install flask \
&& pip3 install flask_restful 



# Set /usr/bin/mongod as the dockerized entry-point application
ENTRYPOINT ["/bin/bash"]