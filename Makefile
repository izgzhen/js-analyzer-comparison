export REMOTE_HOST=tricycle
export REMOTE_DIR=/scratch/zhen/js-tools

deploy:
	python deploy.py

collect:
	scp $(REMOTE_HOST):$(REMOTE_DIR)/results.json .