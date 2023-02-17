const fields = [
    'user_role',
    'name',
    'email',
    'password',
    'confirm_password'
];

const createPayload = () => {
    let payload = {};

    fields.forEach(field => {
        let fieldValue = document.querySelector(
            getQueryStringByType(field)
        ).value;

        payload[field] = fieldValue;
    });

    return payload;
};

const getQueryStringByType = (field) => {
    return field === 'user_role' ?
        `input[name="${field}"]:checked` :
        `input[name="${field}"]`;
};

const submit = () => {
    axios.post('/register', createPayload())
        .then(response => {
            console.log(response.data);
            setAlertWithConfirmation(
                'success',
                {
                    title: 'Usuário cadastrado com sucesso!',
                    text: 'Vá para página de login'
                }
            );
        })
        .catch(error => {
            setAlert('error', getInvalidFieldMessage(error));
        });
};

const getInvalidFieldMessage = (error) => {
    const err = error.response.data.errors;
    const fields = {
        'name': 'Nome',
        'email': 'Email',
        'password': 'Senha',
        'user_role': 'Tipo de usuário',
    };
    const field = Object.keys(err)[0];
    const value = Object.values(err)[0][0];

    return {
        title: fields[field],
        text: value,
    };
};

const setAlert = (type, { title, text }) => {
    Swal.fire({
        title: title,
        text: text,
        icon: type,
        confirmButtonText: 'Ok',
        confirmButtonColor: '#F34444',
    });
};

const setAlertWithConfirmation = (type, { title, text }) => {
    Swal.fire({
        title: title,
        text: text,
        icon: type,
        confirmButtonText: 'Redirecionar',
        confirmButtonColor: '#146C43',
    }).then((result) => {
        if (result) {
            window.location.href = '/login';
        }
    });
};
