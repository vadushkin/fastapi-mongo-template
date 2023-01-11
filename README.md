# Template for connecting FastAPI to MongoDB

Run
---

```
docker-compose up -d
```

### Ports here

```docker-compose.yaml```

```dockerfile
services:
  # Nginx
  web:
    ...
    ports:
      - "8081:80"
  # FastAPI
  app:
    ...
    ports:
      - "8000:8000"
  # MongoDB
  mongo_db:
    ...
    ports:
      - "27017:27017"
```

### Standard Ports

* [Nginx](http://localhost:8081/): 8081
* [FastAPI](http://localhost:8000/): 8000
* MongoDB: 27027