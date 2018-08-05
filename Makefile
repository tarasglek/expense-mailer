all:
	pip install -r requirements.txt -t lib/
freeze:
	ls lib/|grep dist-info|sed 's/.dist-info//'| sed -e  's/-/==/' > requirements.txt
deploy:
	gcloud app deploy
dev:
	dev_appserver.py app.yaml
