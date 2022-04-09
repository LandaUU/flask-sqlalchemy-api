FROM mcr.microsoft.com/mssql/server

WORKDIR /usr/src/app

COPY . /usr/src/app

ENV SA_PASSWORD PHxvf8TEKtrK
ENV ACCEPT_EULA Y
ENV MSSQL_PID Developer

EXPOSE 1433

CMD /bin/bash ./entrypoint.sh