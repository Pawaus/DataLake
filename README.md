# Data Lake
### Flask project with natasha, mongoDB and minio object storaje with S3

To run this app:
1. Install requirements, like ```pip install -r requirements.txt```
2. Pull mongo and minio images from docker hub
```docker pull minio/minio``` and ```docker pull mongo```
3. Run with ```flask run```, specify with ```-h localhost```, where localhost is your ip-address and ```-p 5000``` like port for browse this app

*Recommend to create virtual environment, ```python -m venv venv```*
