import requests

apikey = 'AIzaSyApJgNnb9-1fT8mcY9byyBxAbO7xva9lRY'


def VerifyEmail(idToken):  # verifica se o email é válido dentro do banco e retorna o resultado
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{"requestType":"VERIFY_EMAIL","idToken":"' + idToken + '"}'
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey),
                      headers=headers, data=data)
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    if 'email' in r.json().keys():
        return {'status': 'success', 'email': r.json()['email']}


def novo(email, password):  # cadastra uma nova conta e retorna o idToken
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    # send post request
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={}'.format(apikey), data=details)
    # check for errors in result
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    # if the registration succeeded
    if 'idToken' in r.json().keys():
        return {'status': 'success', 'idToken': r.json()['idToken']}


def entrando(email, password):  # loga com a conta que já existe e retorna o idToken
    details = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    # Post request
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(apikey),
                      data=details)
    # check for errors
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    # success
    if 'idToken' in r.json().keys():
        return {'status': 'success', 'idToken': r.json()['idToken']}


def deletaConta(idToken):  # deleta a conta do usuário usando o idToken
    details = {
        'idToken': idToken
    }
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:delete?key={}'.format(apikey), data=details)
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}

    return {'status': 'success', 'data': r.json()}


def SendResetEmail(email):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {"requestType": "PASSWORD_RESET", "email": email}
    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={}'.format(apikey), data=data)
    if 'error' in r.json().keys():
        return {'status': 'error', 'message': r.json()['error']['message']}
    if 'email' in r.json().keys():
        return {'status': 'success', 'email': r.json()['email']}


# ============================


def logando(email, senha):  # loga com a conta que já existe
    dados = entrando(email, senha)

    if dados['status'] == 'success':
        return 'entrou com sucesso', True
    else:
        if dados['message'] == 'INVALID_PASSWORD':
            return 'senha inválida', False
        else:
            return 'email inválido', False


def resetarSenha(emial):
    resultado = SendResetEmail(emial)

    if resultado['status'] == 'success':
        print('email enviado com sucesso')
    else:
        print('email inválido')
        print(resultado['message'])
