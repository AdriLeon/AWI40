import web
import pyrebase
import firebase_config as token
import json

urls = (
    '/login', 'Login',
    '/signup', 'Signup',
    '/inicio', 'Inicio',
    '/logout', 'Logout',
    '/recuperar', 'Recuperar'
)
app = web.application(urls, globals())
render = web.template.render('views')

class Login: 
    def GET(self):
        try: 
            message = None # se crear una variable para el mensaje de error
            return render.login(message) # renderiza la pagina login.html con el mensaje
        except Exception as error: 
            message = "Error en el sistema" # se almamacena nuestro mensaje de error
            print("Error Login.GET: {}".format(error)) # se imprime el error que ocurrio
            return render.login(message) # se renderiza nuevamente alogin con el mensaje de error

    def POST(self):
        try:
            message = None #se crea una variable para nuestro mensaje de error
            firebase = pyrebase.initialize_app(token.firebaseConfig)
            auth = firebase.auth() # Este nos permitira autenticar con firebase
            formulario = web.input() #tomara los datos del formulario
            email = formulario.email #el email del formulario se almacena en la variable
            password = formulario.password #el password del formulario se almacena en la variable
            print(email,password)#imprimimos el correo y la contraseña para verificar que este tomando los datos
            user = auth.sign_in_with_email_and_password(email, password) # este método devolverá los datos del usuario, incluido un token que puede usar para cumplir con las reglas de seguridad.
            print(user['localId']) #Si los datos son correctos se mostrara la ID del usuario
            web.setcookie('localId', user['localId'], 3600) #creamos la cookie donde se almacena nuestra ID
            print("localId: ", web.cookies().get('localId'))#iprimimos nuestra cookies para verificar que se haya creado
            return web.seeother("inicio") # redirecciona a la pagina de inicio
        except Exception as error:
            format = json.loads(error.args[1]) #presenta el error en formato JSON
            error = format['error'] #Obtenemos el JSON del nuestro error
            message = error['message'] #obtenemos el mensaje
            print("Error Login.POST: {}".format(message))#imprimimos el mensaje 
            web.setcookie('localId', '', 3600)#se elimina la ID de nuestra cookie
            return render.login(message)#renderizamos la pagina, pero mostrando esta vez el mensaje

            
class Signup:
    def GET(self):
        return render.signup()
    def POST(self):
        try:
            firebase = pyrebase.initialize_app(token.firebaseConfig)
            auth = firebase.auth()
            db = firebase.database()
            formulario = web.input()
            name = formulario.name
            phone = formulario.phone
            email = formulario.email
            password = formulario.password
            user= auth.create_user_with_email_and_password(email, password)# nos permitira crear nuevo usuario y contraseña
            print(user['localId']) 
            data = {# se crea una variable, en ella introducirmos los valores del formulario en formato json (un diccionario)
                "name": name,
                "phone": phone,
                "email": email
            }
            results = db.child("users").child(user['localId']).set(data)#aqui almacenaremos los datos en la pase de datos, user para el nombre de la tabla, de ahi generamos otra rama que sera la de la localId
            web.setcookie('localId', user['localId'], 3600)
            print("localId: ", web.cookies().get('localId'))
            return web.seeother("login") # redirecciona a la pagina de login
        except Exception as error:
            format = json.loads(error.args[1])
            error = format['error']
            message = error['message']
            print("Error Login.POST: {}".format(message))
            web.setcookie('localId', '', 3600)
            return render.login(message)

class Inicio:
    def GET(self):
        try:#Se intenta con este codigo
            print("Inicio.GEt localId: ", web.cookies().get('localId'))#imprime la ID de la cookie
            if web.cookies().get('localId') == '': #se verifica si nuestra cookie contiene algun dato
                return web.seeother("login")#si nuestra cookie esta vacia, nos direccionara a la pagina de login
            else:
                return render.inicio()#si contiene datos, se nos renderiza a la pagina de inicio
        except Exception as error:
            print("Error Inicio.GET: {}".format(error)) #si exite un error, se imprime
    def POST(self):
        web.input()#permitira tomar accion del formulario(en este caso el boton que se ha colocado)
        return web.seeother('logout') #nos renderiza a logout


class Logout:
    def GET(self):
        web.setcookie('localId', '', 3600)#eliminara los datos de la ID
        return web.seeother('login')#nos renderiza a la pagina de login

class Recuperar:
    def GET(self):
        return render.recuperar()
    def POST(self):
        firebase = pyrebase.initialize_app(token.firebaseConfig)
        auth = firebase.auth() # Este nos permitira autenticar con firebase
        formulario = web.input() #tomara los datos del formulario
        email = formulario.email #el email del formulario se almacena en la variable
        result = auth.send_password_reset_email(email)
        print(result)
        return web.seeother("login")


if __name__ == "__main__":
    web.config.debug = False
    app.run()