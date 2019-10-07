FROM ubuntu:18.04

# GUI files and File Processing Files
COPY TCR_tool_suite_gui.py /memecos/
COPY descriptions.py /memecos/
COPY MEME.png /memecos/
COPY CIRCOS.png /memecos/
COPY CT044_BML-BM_TCRB.tsv /test-R/
COPY basic_circos_matrices_script.R /memecos/circos_output/
COPY tcr-dist/ /opt/tcr-dist/
 

# Circos and meme tar files
ENV version 0.69-9
ADD http://circos.ca/distribution/circos-${version}.tgz /tmp/
ADD http://circos.ca/distribution/circos-tools-0.23.tgz /tmp/
COPY meme-5.0.5.tar.gz /tmp/

# Make Apt non-interactive
ARG DEBIAN_FRONTEND=noninteractive

# Set PATH variable
RUN export PATH=$PATH:/usr/local/bin

# Install Python dependencies
RUN apt-get update \
    && apt-get install -y build-essential make wget libxml-simple-perl git \
    libjpeg-dev libfreetype6-dev libreadline-gplv2-dev libncursesw5-dev \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
# Install Tkinter and PIL
    python3-pil python3-pil.imagetk python3-tk

# Install MEME dependencies 
RUN apt-get update && apt-get install -y \
    libopenmpi-dev \
    openmpi-bin \
    ghostscript \
    libgs-dev \
    libgd-dev \
    libexpat1-dev \
    zlib1g-dev \
    libxml2-dev \
    autoconf automake libtool \
    libhtml-template-compiled-perl \
    libxml-opml-simplegen-perl \
    libxml-libxml-debugging-perl \
    sudo \
    openssh-server

# Circos Perl dependencies
RUN cpan App::cpanminus
RUN cpanm List::MoreUtils Math::Bezier Math::Round Math::VecStat Params::Validate Readonly Regexp::Common SVG Set::IntSpan \ 
    Statistics::Basic Text::Format Clone Config::General Font::TTF::Font GD Statistics::Descriptive
# MEME perl dependencies
RUN PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install Log::Log4perl' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install Math::CDF' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install CGI' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install HTML::PullParser' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install HTML::Template' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Simple' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Parser::Expat' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::LibXML' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::LibXML::Simple' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Compile' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Compile::SOAP11' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Compile::WSDL11' \
    && PERL_MM_USE_DEFAULT=1 perl -MCPAN -e 'install XML::Compile::Transport::SOAPHTTP'

# Install R
RUN apt-get update \
    && apt-get install -y r-base-dev
 
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
    && tar zxvf /tmp/meme-5.0.5.tar.gz \
    && mv meme-5.0.5 meme  && cd meme \
    && ./configure --prefix=/opt/meme  --enable-build-libxml2 --enable-build-libxslt  --with-url=http://meme-suite.org \
    && make \
    && make install \
    && mkdir /memecos/meme_out 

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
CMD ["memecos/TCR_tool_suite_gui.py"] 
