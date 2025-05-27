FROM python:slim
RUN pip install Flask
RUN pip install gunicorn
RUN pip install python-dotenv
RUN pip install python-dateutil
COPY . /srv
WORKDIR /srv
ENV FLASK_APP=app
EXPOSE 5000
RUN ["chmod", "+x", "/srv/entrypoint.sh"]
CMD ["/srv/entrypoint.sh"]