FROM python:3.14.2-alpine@sha256:7af51ebeb83610fb69d633d5c61a2efb87efa4caf66b59862d624bb6ef788345 AS python
# The remote Dockerfile is different, but the official solution works on both the local and the remote without any changes.
# docker run -p 5000:5000 --privileged $(docker build -q .)
# If you are running ubuntu please run the following commands to run redpwn/jail:
# sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0
# sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
FROM redpwn/jail
COPY --from=python / /srv
COPY server.py /srv/app/run
ENV JAIL_TIME=120 JAIL_MEM=20M JAIL_CPU=100