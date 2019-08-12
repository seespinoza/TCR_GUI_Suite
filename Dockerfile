FROM ubuntu:18.04

# GUI files and File Processing Files
COPY tkinterSandBox.py /memecos/
COPY test.sh /memecos/
COPY MEME.png /memecos/
COPY CIRCOS.png /memecos/
COPY CT044_BML-BM_TCRB.tsv /test-R/
COPY basic_circos_matrices_script.R /memecos/circos_output/
COPY tcr-dist/ /opt/tcr-dist/

# Circos and meme tar files
ENV version 0.69-9
ADD http://circos.ca/distribution/circos-${version}.tgz /tmp/
ADD http://circos.ca/distribution/circos-tools-0.23.tgz /tmp/
ADD http://meme-suite.org/meme-software/5.0.5/meme-5.0.5.tar.gz /tmp/

ADD https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz /tmp/
# Make Apt non-interactive
ARG DEBIAN_FRONTEND=noninteractive

# Set PATH variable
RUN export PATH=$PATH:/usr/local/bin

# Install Circos dependencies
RUN apt-get update \
    && apt-get install -y build-essential make wget libgd-dev libxml-simple-perl git \
    libgd-dev libjpeg-dev libfreetype6-dev python3-pil python3-pil.imagetk \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN cpan App::cpanminus
RUN cpanm List::MoreUtils Math::Bezier Math::Round Math::VecStat Params::Validate Readonly Regexp::Common SVG Set::IntSpan Statistics::Basic Text::Format Clone Config::General Font::TTF::Font GD Statistics::Descriptive

# Install R
RUN apt-get update \
    && apt-get install -y r-base-dev
 
# Install MEME dependencies

# Install tkinter module
RUN apt-get update \
    && apt-get install -y python3-tk \
    && apt-get install -y sudo

# Install Circos and Circos tools
RUN cd /opt/ \
    && tar xzvf /tmp/circos-${version}.tgz \
    && mv circos-${version} circos \
    && mkdir /memecos/circos_output/img/ \
    && tar xzvf /tmp/circos-tools-0.23.tgz \
    && mv circos-tools-0.23 circos-tools

COPY all.conf /opt/circos-tools/tools/tableviewer/data/

# Install MEME
RUN cd /opt/ \
    && tar xzvf /tmp/meme-5.0.5.tar.gz \
    && mv meme-5.0.5 meme
# Install tcr dist dependancies
RUN apt-get update \
    && apt-get install -y python python-numpy python-scipy python-matplotlib python-pip \
    && pip install -U scikit-learn \
    && cd /opt/tcr-dist/ \
    && python setup.py  
# DISPLAY SETTINGS
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/developer && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer 

RUN chmod -R 777 /opt/
USER developer
ENV HOME /home/developer

ENTRYPOINT ["/usr/bin/python3"]
CMD ["memecos/tkinterSandBox.py"] 
