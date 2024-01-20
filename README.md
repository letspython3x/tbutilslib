# Installation of the library
```
cd tbutilslib
pip install .
```

# Database Setup

## Pull the Docker Image:
```docker pull mongodb/mongodb-community-server```

## Run the docker image on host “0.0.0.0” port 27017
```docker run -d -p 27017:27017 --name mongo-db mongodb/mongodb-community-server```

## Take entry into the mongo shell
```docker exec -it mongo mongosh```

## MongoDb Commands:
```
use Stockmarket
show collections
```

# Connection with Python
```
from mongoengine import connect, disconnect
from tbutilslib.config.database import MongoConfig
connect(MongoConfig.MONGODB_DB, host='0.0.0.0', port=27017)
from src.tbutilslib.models import AdvanceDeclineCollection
AdvanceDeclineCollection.create_index(['timestamp'], unique=True)
```
