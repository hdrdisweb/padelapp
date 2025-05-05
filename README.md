PadelAPP
Gestor web de equipos, partidos y convocatorias para clubes y jugadores de pádel.
Desarrollado como proyecto final del curso de Python y Django.
________________________________________
📚 Descripción
PadelAPP es una aplicación web que permite:
•	Gestionar equipos y jugadores.
•	Crear convocatorias para competiciones (LAPA, SNP).
•	Inscribir y alinear jugadores en pistas.
•	Compartir las convocatorias por WhatsApp.
Proyecto desarrollado usando Django, aplicando los conceptos aprendidos durante el curso.
________________________________________
🚀 Tecnologías usadas
•	Python 3
•	Django
•	HTML, CSS, JS
•	Django Templates con herencia
•	Django Forms para validación
________________________________________
🗄️ Modelos principales
•	Equipo: representa cada equipo de pádel.
•	Jugador: relacionado a un equipo.
•	Convocatoria: para organizar partidos oficiales.
•	AlineacionConvocatoria: relación entre jugadores y convocatorias.
(Relaciones hechas con el ORM de Django)
________________________________________
📄 Funcionalidades (Requisitos cumplidos)
•	✅ Mínimo 3 vistas (listado de equipos, detalle de convocatorias, gestión de alineaciones).
•	✅ Uso de plantillas con herencia (base.html, content.html).
•	✅ 2+ modelos relacionados usando ORM.
•	✅ Formularios validados con Django Forms.
•	✅ CRUD completo sobre equipos y convocatorias.
•	✅ Estáticos: CSS propio + JS para drag & drop.
________________________________________
🛠️ Instalación y ejecución local
1.	Clona el repositorio
git clone https://github.com/hdrdisweb/padelapp
cd padelapp
2.	Crea un entorno virtual y actívalo
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
3.	Instala dependencias
pip install -r requirements.txt
4.	Migra la base de datos
python manage.py migrate
5.	Corre el servidor
python manage.py runserver
Accede a la app en http://localhost:8000
________________________________________
👨‍💻 Autor
Proyecto desarrollado por Darío Roma, como prueba final del curso de Python y Django.
________________________________________
📞 Contacto
darioroma@gmail.com
________________________________________
🏓 Nota
Este proyecto es una versión básica para fines educativos. En producción, se encuentra desplegado en un servidor VPS propio. Visita:  https://padelapp.xn--hdrdiseoweb-7db.es/

