# app-01
Digital Ocean's App that works as a reverse proxy with the SSO autentication process.

### Ambinete de desenvolvimento
Inicialize o ambiente de desenvolvimento com o comando:
```
$ docker-compose up -d
```

Execute o comando abaixo para instalar as dependências do projeto:
```
$ docker exec -it app-01 pip install -r requirements.txt
```

Execute o comando abaixo para rodar o projeto
```
$ docker exec -it python npp-app-02.py
```


### Referências

Serveless na Digital Ocean:
- https://docs.digitalocean.com/products/functions/getting-started/sample-functions/

Serveless Runtime Python Functions na Digital Ocean:
- https://docs.digitalocean.com/products/functions/reference/runtimes/python/

Digital Ocean Runtimes:
- https://docs.digitalocean.com/products/functions/reference/runtimes/
- https://docs.digitalocean.com/products/functions/reference/runtimes/python/

