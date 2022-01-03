FROM ubuntu
RUN yes | unminimize
RUN adduser user
RUN apt-get update && apt-get install -y python3 build-essential
CMD ["/bin/bash"]
