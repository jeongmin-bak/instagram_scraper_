FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/jeongmin-bak/instagram_scraper.git

WORKDIR /home/instagram_scraper/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN echo "SECRET_KEY=django-insecure-6@&7*^y97x@@3k4-vf-+)5g^!q=z0lt*m9q)#nents+marm+x)" > .env
RUN python manage.py migrategh pr checkout 1

EXPOSE 8000

CMD ["gunicorn", "instagram_scraper.wsgi", "--bind", "0.0.0.0:8000"]

ddd