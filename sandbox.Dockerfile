FROM ubuntu
RUN yes | unminimize
RUN adduser user
CMD ["/bin/bash"]
