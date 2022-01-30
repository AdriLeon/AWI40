import web
import pyrebase
import firebase_config as token

urls = (
    '/login', 'Login',
    '/signup', 'Signup',
)
app = web.application(urls, globals())
render = web.template.render('views')

class Login:
    def GET(self):
       return render.login()
    def POST(self):
        firebase = pyrebase.initialize_app(token.firebaseConfig)
        auth = firebase.auth() # Este nos permitira autenticar con firebase
        formulario = web.input() #tomara los datos del formulario
        email = formulario.email #el email del formulario se almacena en la variable
        password = formulario.password #el password del formulario se almacena en la variable
        user = auth.sign_in_with_email_and_password(email, password) # este método devolverá los datos del usuario, incluido un token que puede usar para cumplir con las reglas de seguridad.
        print(user['localId']) #Si los datos son correctos se mostrara la ID del usuario
        return render.login() # regresa a la pantalla de login

class Signup:
    def GET(self):
        return render.signup()
    def POST(self):
        firebase = pyrebase.initialize_app(token.firebaseConfig)
        auth = firebase.auth()
        formulario = web.input()
        email = formulario.email
        password = formulario.password
        user= auth.create_user_with_email_and_password(email, password)# no permitira crear nuevo usuario y contraseña
        print(user['localId']) 
        return render.signup()

if __name__ == "__main__":
    app.run()