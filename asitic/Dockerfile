FROM i386/centos:latest

RUN yum install -y libXext.i686 compat-libf2c-34.i686

RUN curl http://rfic.eecs.berkeley.edu/~niknejad/Asitic/grackle/asitic_linux.gz > asitic_linux.gz && \
        gzip -d asitic_linux.gz && \
        chmod +x asitic_linux
