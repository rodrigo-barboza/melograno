# Melograno
A django project called Melhograno which is a delivery system inspired by ifood

## Links
- [Trello](https://trello.com/invite/projetosistemasdistribuidos2/ATTI9cdfb6bff6b7b7968c0b2e3e5af19485AF69AC37)

- [Mockup (figma)](https://www.figma.com/file/cRtzvhDKHlpHD0bp1EYQB0/Melograno-Project?node-id=0%3A1)

- [Padrões de projeto](https://ringed-viper-289.notion.site/Especifica-es-t-cnicas-para-Sistemas-Distribu-dos-c4140bd7b71b48b3982f6365a24a6cf2)

## Padrões do projeto
- Nomes de classes: PascalCase
- Nomes de métodos e variáveis: snake_case

## Setup de instalação
Tendo o vagrant já instalado e configurado na máquina, vá até a pasta web-folder e execute o seguinte comando:
```
git clone https://github.com/rodrigo-barboza/melograno.git
```

Feito isto, entre na pasta do projeto:
  ```
  cd melograno
  ```

Feito isto, abra o projeto no seu VSC:
  ```
  code .
  ```

Para rodar o servidor, abra outro terminal (ou aba), vá em "sd", digite o seguinte comando para subir o vagrant:
  ```
  vagrant up
  ```

Em seguida, digite o seguinte comando para entrar no bash do vagrant:
  ```
  vagrant ssh
  ```

Feito isso, digite o seguinte comando para iniciar o server django;
  ```
  cd /vagrant/web-folder/melograno/` (para entrar na pasta do projeto)
  ```
  ```
  python manage.py runserver 0:8000` (para iniciar o servidor do django)
  ```

Obs: fechar o terminal vai matar o processo do servidor e consequentemente ele vai parar, por isso é recomendável deixar em outro terminal.

Feito isso, você já deve poder acessar a aplicação django no seguinte endereço: http://192.168.56.120:8000/
